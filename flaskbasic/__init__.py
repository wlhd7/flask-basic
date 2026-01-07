"""Application factory for the flaskbasic project."""

from __future__ import annotations

import os
from pathlib import Path

import click
from dotenv import load_dotenv
from flask import Flask

from .config import get_config
from .extensions import db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application instance."""

    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    config_name = config_name or os.getenv("FLASK_CONFIG", "development")
    app = Flask(__name__.split(".")[0])
    app.config.from_object(get_config(config_name))

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register application blueprints."""

    from .auth import bp as auth_bp
    from .main import bp as main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)


def register_shellcontext(app: Flask) -> None:
    """Register objects for `flask shell`."""

    from . import models

    @app.shell_context_processor
    def shell_context():
        return {"db": db, "User": models.User}


def register_commands(app: Flask) -> None:
    """Register custom CLI commands."""

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Create database tables in the configured database."""

        with app.app_context():
            db.create_all()
        click.echo("Database tables created.")
