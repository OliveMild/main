#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello World\n")
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found\n")

    def log_message(self, format, *args):
        # Suppress default per-request console logging
        pass


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), HelloHandler)
    print("Serving on http://127.0.0.1:8000")
    server.serve_forever()
