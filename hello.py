#!/usr/bin/env python3

import http.server
import socketserver

PORT = 8000


class HelloHandler(http.server.BaseHTTPRequestHandler):
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
            self.wfile.write(b"404 Not Found\n")

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HelloHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
