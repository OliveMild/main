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
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data["error"] == "Not found"
    assert "message" in data


def test_item_not_found_returns_json_404(client):
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data["error"] == "Item not found"
    assert data["item_id"] == 9999


def test_existing_item_returns_200(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data["item_id"] == 1
    assert data["name"] == "apple"
