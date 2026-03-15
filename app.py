#!/usr/bin/env python3
"""Simple Flask web application with proper 404 error handling."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Return a welcome message."""
    return jsonify({"message": "Hello World"})


@app.route("/health")
def health():
    """Return application health status."""
    return jsonify({"status": "ok"})


@app.errorhandler(404)
def not_found(error):
    """Return a JSON 404 error response instead of the default HTML page."""
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404


if __name__ == "__main__":
    app.run()
