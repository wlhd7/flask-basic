"""WSGI entry point for the flaskbasic project."""

from flaskbasic import create_app

app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run()
