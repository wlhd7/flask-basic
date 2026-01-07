"""Pytest fixtures for the flaskbasic project."""

from __future__ import annotations

import pytest

from flaskbasic import create_app
from flaskbasic.extensions import db


@pytest.fixture()
def app():
    """Create a new app instance for each test."""

    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Return a Flask test client."""

    return app.test_client()


@pytest.fixture()
def runner(app):
    """Return a CLI runner for invoking custom commands."""

    return app.test_cli_runner()
