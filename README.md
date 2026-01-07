# Flask Basic Starter

A minimal Flask starter template wired for MySQL, session-based authentication, database migrations, and basic testing.

## Features

- Application factory with environment-aware configuration loading via `.env`
- SQLAlchemy ORM models and Flask-Migrate migrations targeting MySQL
- Built-in authentication blueprint using Flask-Login, Flask-WTF, and bcrypt password hashing
- Minimal Jinja templates and CSS to support login, registration, and a protected dashboard view
- Pytest test suite covering registration and login flows

## Getting Started

### Prerequisites

- Python 3.11+ (tested with 3.13.3)
- A running MySQL instance or Docker container

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your MySQL credentials or override `DATABASE_URL` using another SQLAlchemy URI (e.g., SQLite for local development).

### Database Migration Commands

```bash
flask db init      # first time only
flask db migrate -m "Initial migration"
flask db upgrade
```

### Run the App

```bash
flask --app wsgi run
```

Open http://127.0.0.1:5000 in a browser. Register a new account, then log in to view the protected dashboard.

### Tests

```bash
pytest
```

## Project Structure

```
flaskbasic/
  __init__.py
  auth/
  main/
  models.py
  templates/
  static/
  extensions.py
  config.py
migrations/
tests/
wsgi.py
```

## Deployment Notes

- Set `FLASK_CONFIG=production`, provide a strong `SECRET_KEY`, and configure TLS for session cookies.
- Serve via `gunicorn` or another WSGI server behind a reverse proxy (e.g., Nginx).
- Consider Dockerizing MySQL and the Flask app for reproducible deployments.
