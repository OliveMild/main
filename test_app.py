#!/usr/bin/env python3
"""Tests for the HTTP application."""

import json
import threading
from http.client import HTTPConnection
from http.server import HTTPServer

import pytest

from app import AppHandler, ROUTES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _TestServer:
    """Lightweight wrapper that starts AppHandler in a background thread."""

    def __init__(self):
        self.server = HTTPServer(("127.0.0.1", 0), AppHandler)
        self.port = self.server.server_address[1]
        self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *_):
        self.server.shutdown()

    def get(self, path: str):
        conn = HTTPConnection("127.0.0.1", self.port)
        conn.request("GET", path)
        resp = conn.getresponse()
        body = json.loads(resp.read().decode())
        conn.close()
        return resp.status, body


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestKnownRoutes:
    def test_root_returns_200(self):
        with _TestServer() as srv:
            status, _ = srv.get("/")
            assert status == 200

    def test_root_body(self):
        with _TestServer() as srv:
            _, body = srv.get("/")
            assert body == ROUTES["/"]

    def test_health_returns_200(self):
        with _TestServer() as srv:
            status, _ = srv.get("/health")
            assert status == 200

    def test_health_body(self):
        with _TestServer() as srv:
            _, body = srv.get("/health")
            assert body == ROUTES["/health"]


class TestNotFoundHandling:
    def test_unknown_path_returns_404(self):
        with _TestServer() as srv:
            status, _ = srv.get("/does-not-exist")
            assert status == 404

    def test_unknown_path_body_contains_error(self):
        with _TestServer() as srv:
            _, body = srv.get("/missing")
            assert body["error"] == "Not Found"

    def test_unknown_path_body_contains_path(self):
        with _TestServer() as srv:
            _, body = srv.get("/missing")
            assert body["path"] == "/missing"

    def test_nested_unknown_path_returns_404(self):
        with _TestServer() as srv:
            status, _ = srv.get("/a/b/c")
            assert status == 404

    def test_content_type_is_json_on_404(self):
        with _TestServer() as srv:
            conn = HTTPConnection("127.0.0.1", srv.port)
            conn.request("GET", "/nope")
            resp = conn.getresponse()
            conn.close()
            assert "application/json" in resp.getheader("Content-Type", "")
