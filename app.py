#!/usr/bin/env python3
"""Simple HTTP application with proper 404 error handling."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


ROUTES = {
    "/": {"message": "Welcome to the application!"},
    "/health": {"status": "ok"},
}


class AppHandler(BaseHTTPRequestHandler):
    """Request handler that serves registered routes and returns 404 for unknown paths."""

    def do_GET(self):
        if self.path in ROUTES:
            body = json.dumps(ROUTES[self.path]).encode()
            self._send_response(200, body)
        else:
            body = json.dumps({"error": "Not Found", "path": self.path}).encode()
            self._send_response(404, body)

    def _send_response(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A002
        pass  # suppress default request logging


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Start the HTTP server."""
    server = HTTPServer((host, port), AppHandler)
    print(f"Serving on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
