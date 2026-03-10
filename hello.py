#!/usr/bin/env python3

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


def greet(name=None):
    """Return a greeting message.

    Args:
        name: Optional name to include in the greeting.

    Returns:
        A greeting string.
    """
    if name:
        return f"Hello, {name}!"
    return "Hello, World!"


class HelloHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Hello World application."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(greet().encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def log_message(self, format, *args):
        """Suppress default request logging."""
        pass


def run_server(host="127.0.0.1", port=8000):
    """Start the HTTP server.

    Args:
        host: Host address to bind to.
        port: Port number to listen on.
    """
    server = HTTPServer((host, port), HelloHandler)
    print(f"Server running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "greet":
        name = args[1] if len(args) > 1 else None
        print(greet(name))
    else:
        run_server()
