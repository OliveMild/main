#!/usr/bin/env python3
"""Tests for app.py — Flask web application."""

import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------


class TestIndex:
    def test_status_ok(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_returns_json(self, client):
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_welcome_message(self, client):
        data = client.get("/").get_json()
        assert data["message"] == "Welcome to the application"
        assert data["status"] == "ok"


# ---------------------------------------------------------------------------
# GET /items
# ---------------------------------------------------------------------------


class TestListItems:
    def test_status_ok(self, client):
        response = client.get("/items")
        assert response.status_code == 200

    def test_returns_json(self, client):
        response = client.get("/items")
        assert response.content_type == "application/json"

    def test_items_key_present(self, client):
        data = client.get("/items").get_json()
        assert "items" in data

    def test_items_is_a_list(self, client):
        data = client.get("/items").get_json()
        assert isinstance(data["items"], list)


# ---------------------------------------------------------------------------
# GET /items/<id>
# ---------------------------------------------------------------------------


class TestGetItem:
    def test_existing_item_returns_200(self, client):
        response = client.get("/items/1")
        assert response.status_code == 200

    def test_existing_item_data(self, client):
        data = client.get("/items/1").get_json()
        assert data["id"] == 1
        assert "name" in data

    def test_missing_item_returns_404(self, client):
        response = client.get("/items/9999")
        assert response.status_code == 404

    def test_missing_item_error_message(self, client):
        data = client.get("/items/9999").get_json()
        assert "error" in data
        assert data["item_id"] == 9999

    def test_missing_item_returns_json(self, client):
        response = client.get("/items/9999")
        assert response.content_type == "application/json"


# ---------------------------------------------------------------------------
# 404 handler — unmatched routes
# ---------------------------------------------------------------------------


class TestNotFoundHandler:
    def test_unknown_route_returns_404(self, client):
        response = client.get("/does-not-exist")
        assert response.status_code == 404

    def test_unknown_route_returns_json(self, client):
        response = client.get("/does-not-exist")
        assert response.content_type == "application/json"

    def test_unknown_route_error_key(self, client):
        data = client.get("/does-not-exist").get_json()
        assert "error" in data

    def test_unknown_nested_route_returns_404(self, client):
        response = client.get("/some/nested/path")
        assert response.status_code == 404

    def test_unknown_post_route_returns_404(self, client):
        response = client.post("/no-such-endpoint")
        assert response.status_code == 404
