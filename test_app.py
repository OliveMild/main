#!/usr/bin/env python3
import pytest

from hello import greet
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_greet_default():
    assert greet() == "Hello World"


def test_greet_with_name():
    assert greet("Alice") == "Hello Alice"


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello World"


def test_greet_name_route(client):
    response = client.get("/greet/Bob")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello Bob"


def test_404_handler(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Not found"
