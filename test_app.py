#!/usr/bin/env python3
"""Tests for the Flask web application in app.py."""

import unittest

from app import app


class TestIndexRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_returns_json(self):
        response = self.client.get("/")
        self.assertEqual(response.content_type, "application/json")

    def test_index_message(self):
        response = self.client.get("/")
        data = response.get_json()
        self.assertEqual(data["message"], "Hello, World!")


class TestGreetRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_greet_returns_200(self):
        response = self.client.get("/greet/Alice")
        self.assertEqual(response.status_code, 200)

    def test_greet_message(self):
        response = self.client.get("/greet/Alice")
        data = response.get_json()
        self.assertEqual(data["message"], "Hello, Alice!")

    def test_greet_world(self):
        response = self.client.get("/greet/World")
        data = response.get_json()
        self.assertEqual(data["message"], "Hello, World!")


class TestNotFoundHandler(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_unknown_route_returns_404(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

    def test_unknown_route_returns_json(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.content_type, "application/json")

    def test_unknown_route_error_field(self):
        response = self.client.get("/nonexistent")
        data = response.get_json()
        self.assertEqual(data["error"], "Not Found")

    def test_unknown_route_message_field_present(self):
        response = self.client.get("/nonexistent")
        data = response.get_json()
        self.assertIn("message", data)

    def test_nested_unknown_route_returns_404(self):
        response = self.client.get("/does/not/exist")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
