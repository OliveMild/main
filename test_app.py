#!/usr/bin/env python3
"""Tests for the Flask application routes and 404 error handling."""

import unittest

from app import app


class TestIndexRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_index_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_returns_json(self):
        response = self.client.get("/")
        self.assertEqual(response.content_type, "application/json")

    def test_index_contains_message(self):
        response = self.client.get("/")
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Hello World")


class TestHealthRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_health_returns_200(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_health_returns_json(self):
        response = self.client.get("/health")
        self.assertEqual(response.content_type, "application/json")

    def test_health_status_ok(self):
        response = self.client.get("/health")
        data = response.get_json()
        self.assertEqual(data["status"], "ok")


class Test404ErrorHandler(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_unknown_route_returns_404(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

    def test_404_response_is_json(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.content_type, "application/json")

    def test_404_response_contains_error_key(self):
        response = self.client.get("/nonexistent")
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not Found")

    def test_404_response_contains_message(self):
        response = self.client.get("/nonexistent")
        data = response.get_json()
        self.assertIn("message", data)

    def test_deeply_nested_missing_route_returns_404(self):
        response = self.client.get("/a/b/c/d")
        self.assertEqual(response.status_code, 404)

    def test_post_to_missing_route_returns_404(self):
        response = self.client.post("/nonexistent")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
