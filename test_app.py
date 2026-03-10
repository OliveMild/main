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
    assert data["message"] == "Hello, World!"


def test_greet_with_name(client):
    response = client.get("/greet/Alice")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello, Alice!"


def test_unknown_route_returns_404(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data["error"] == "Not found"
    assert data["status"] == 404
