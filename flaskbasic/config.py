"""Configuration objects for the flaskbasic project."""

from __future__ import annotations

import os


class BaseConfig:
    """Base application configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/flaskbasic"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # one week
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class DevelopmentConfig(BaseConfig):
    """Configuration overrides for local development."""

    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(BaseConfig):
    """Configuration used for running the automated test suite."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///:memory:"
    )


class ProductionConfig(BaseConfig):
    """Configuration suitable for deployment."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str) -> type[BaseConfig]:
    """Look up a configuration class by name."""

    try:
        return CONFIG_MAP[name]
    except KeyError as exc:
        available = ", ".join(sorted(CONFIG_MAP))
        raise KeyError(f"Unknown config '{name}'. Expected one of: {available}") from exc
