"""Tests for custom 404 error handling in app.py."""

import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_404_unknown_route_returns_json(client):
    """Accessing an unknown route should return a JSON 404 response."""
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Not found"
    assert "message" in data


def test_404_content_type_is_json(client):
    """The 404 response Content-Type should be application/json."""
    response = client.get("/does-not-exist")
    assert response.content_type.startswith("application/json")


def test_get_existing_item(client):
    """Accessing a known item should return 200 with item data."""
    response = client.get("/items/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["item_id"] == 1
    assert "name" in data


def test_get_missing_item_returns_json_404(client):
    """Accessing a non-existent item should return a JSON 404."""
    response = client.get("/items/9999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Item not found"
    assert data["item_id"] == 9999


def test_index_returns_greeting(client):
    """The root route should return a JSON greeting."""
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
