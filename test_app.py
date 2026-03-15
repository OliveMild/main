#!/usr/bin/env python3
"""Unit tests for the app module."""

import io
import threading
import unittest
import urllib.request
from http.server import HTTPServer

from app import AppRequestHandler, handle_request, run


class TestHandleRequest(unittest.TestCase):
    """Tests for the handle_request routing function."""

    # --- known routes ---

    def test_index_returns_200(self):
        status, _, _ = handle_request("/")
        self.assertEqual(status, 200)

    def test_index_body_not_empty(self):
        _, _, body = handle_request("/")
        self.assertTrue(body)

    def test_hello_returns_200(self):
        status, _, _ = handle_request("/hello")
        self.assertEqual(status, 200)

    def test_hello_body_contains_hello(self):
        _, _, body = handle_request("/hello")
        self.assertIn("Hello", body)

    # --- unknown routes return 404 ---

    def test_unknown_path_returns_404(self):
        status, _, _ = handle_request("/does-not-exist")
        self.assertEqual(status, 404)

    def test_unknown_path_body_contains_404(self):
        _, _, body = handle_request("/does-not-exist")
        self.assertIn("404", body)

    def test_unknown_path_with_query_string_returns_404(self):
        status, _, _ = handle_request("/missing?foo=bar")
        self.assertEqual(status, 404)

    def test_deeply_nested_unknown_path_returns_404(self):
        status, _, _ = handle_request("/a/b/c/d")
        self.assertEqual(status, 404)

    def test_trailing_slash_on_hello_returns_404(self):
        status, _, _ = handle_request("/hello/")
        self.assertEqual(status, 404)

    # --- content type ---

    def test_index_content_type(self):
        _, content_type, _ = handle_request("/")
        self.assertEqual(content_type, "text/plain")

    def test_404_content_type(self):
        _, content_type, _ = handle_request("/nope")
        self.assertEqual(content_type, "text/plain")


class TestAppRequestHandler(unittest.TestCase):
    """Integration tests exercising the HTTP server end-to-end."""

    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), AppRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path):
        url = f"http://127.0.0.1:{self.port}{path}"
        try:
            with urllib.request.urlopen(url) as resp:
                return resp.status, resp.read().decode()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode()

    def test_get_index_200(self):
        status, _ = self._get("/")
        self.assertEqual(status, 200)

    def test_get_hello_200(self):
        status, _ = self._get("/hello")
        self.assertEqual(status, 200)

    def test_get_unknown_404(self):
        status, _ = self._get("/nonexistent")
        self.assertEqual(status, 404)

    def test_get_unknown_body_contains_404(self):
        _, body = self._get("/nonexistent")
        self.assertIn("404", body)


if __name__ == "__main__":
    unittest.main()
