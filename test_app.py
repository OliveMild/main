import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello World"


def test_404_unknown_route(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not found"
    assert data["status"] == 404


def test_404_response_is_json(client):
    response = client.get("/does-not-exist")
    assert response.content_type == "application/json"


def test_405_method_not_allowed(client):
    response = client.delete("/")
    assert response.status_code == 405
    data = response.get_json()
    assert data["error"] == "Method not allowed"
    assert data["status"] == 405
