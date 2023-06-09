from flask import Flask
import pytest
from flask.testing import FlaskClient
from .app import app as _app


@pytest.fixture(autouse=True)
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def app():
    yield _app
