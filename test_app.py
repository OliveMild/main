import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_unknown_route_returns_json_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Not found"
    assert "message" in data


def test_missing_item_returns_json_404(client):
    response = client.get("/items/9999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Item not found"
    assert data["item_id"] == 9999


def test_existing_item_returns_200(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["item_id"] == 1
    assert data["name"] == "Widget"
