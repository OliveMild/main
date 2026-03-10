#!/usr/bin/env python3
"""Tests for the Flask web application in app.py."""

import json
import unittest

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_index_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_returns_world_greeting(self):
        response = self.client.get("/")
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Hello, World!")

    def test_greet_name_returns_200(self):
        response = self.client.get("/greet/Alice")
        self.assertEqual(response.status_code, 200)

    def test_greet_name_returns_custom_greeting(self):
        response = self.client.get("/greet/Alice")
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Hello, Alice!")

    def test_unknown_route_returns_404(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

    def test_unknown_route_returns_json_error(self):
        response = self.client.get("/nonexistent")
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Not found")


class TestGreet(unittest.TestCase):
    def test_greet_default(self):
        from hello import greet
        self.assertEqual(greet(), "Hello, World!")

    def test_greet_custom_name(self):
        from hello import greet
        self.assertEqual(greet("Alice"), "Hello, Alice!")


if __name__ == "__main__":
    unittest.main()
