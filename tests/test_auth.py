"""Authentication flow tests."""

from __future__ import annotations

from flaskbasic.extensions import db
from flaskbasic.models import User


def test_register_creates_user(client):
    response = client.post(
        "/auth/register",
        data={
            "email": "user@example.com",
            "password": "strongpassword",
            "confirm_password": "strongpassword",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Account created" in response.data
    assert User.query.filter_by(email="user@example.com").first() is not None


def test_login_with_valid_credentials(client):
    user = User(email="user@example.com")
    user.set_password("strongpassword")
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        data={"email": "user@example.com", "password": "strongpassword"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Welcome back" in response.data


def test_login_rejects_invalid_password(client):
    user = User(email="user@example.com")
    user.set_password("strongpassword")
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        data={"email": "user@example.com", "password": "wrong"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data
