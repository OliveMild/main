"""Tests for the Flask application and its 404 error handler."""

import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_index_returns_greeting(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello, World!"


def test_greet_name_returns_greeting(client):
    response = client.get("/greet/Alice")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello, Alice!"


def test_unknown_route_returns_404(client):
    response = client.get("/nonexistent-page")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not found"
    assert data["status"] == 404


def test_unknown_nested_route_returns_404(client):
    response = client.get("/some/deep/path")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not found"
    assert data["status"] == 404


def test_404_response_is_json(client):
    response = client.get("/does-not-exist")
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data["error"] == "Not found"
    assert data["status"] == 404
