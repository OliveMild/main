#!/usr/bin/env python3
"""Simple HTTP application with route handling and 404 error support."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


def get_routes():
    """Return the mapping of URL paths to handler functions."""
    return {
        "/": _handle_index,
        "/hello": _handle_hello,
    }


def _handle_index():
    """Return the response for the index route."""
    return 200, "text/plain", "Welcome to the application."


def _handle_hello():
    """Return the response for the hello route."""
    return 200, "text/plain", "Hello World"


def handle_request(path):
    """Dispatch *path* to the appropriate handler.

    Returns a (status_code, content_type, body) tuple.  Unrecognised paths
    yield a 404 response so that callers never receive an unhandled error.
    """
    routes = get_routes()
    parsed_path = urlparse(path).path
    handler = routes.get(parsed_path)
    if handler is None:
        return 404, "text/plain", f"404 Not Found: {parsed_path}"
    return handler()


class AppRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler that delegates to :func:`handle_request`."""

    def do_GET(self):
        status, content_type, body = handle_request(self.path)
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):  # noqa: A002
        """Suppress default access-log output during tests."""


def run(host="127.0.0.1", port=8080):
    """Start the HTTP server on *host*:*port*."""
    server = HTTPServer((host, port), AppRequestHandler)
    print(f"Serving on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
