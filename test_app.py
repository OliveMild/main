#!/usr/bin/env python3
"""Tests for the Flask web application."""

import unittest

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_index_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_returns_hello_world(self):
        response = self.client.get("/")
        data = response.get_json()
        self.assertEqual(data["message"], "Hello World")

    def test_unknown_route_returns_404(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

    def test_404_response_is_json(self):
        response = self.client.get("/nonexistent")
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not Found")


if __name__ == "__main__":
    unittest.main()
