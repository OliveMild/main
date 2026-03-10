#!/usr/bin/env python3
"""Simple Flask web application with proper 404 error handling."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Return a welcome message."""
    return jsonify({"message": "Hello, World!"})


@app.route("/greet/<name>")
def greet(name):
    """Return a personalized greeting for *name*."""
    return jsonify({"message": f"Hello, {name}!"})


@app.errorhandler(404)
def not_found(error):
    """Return a JSON 404 response for unknown routes."""
    return jsonify({"error": "Not Found", "message": str(error)}), 404


if __name__ == "__main__":
    import os

    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
