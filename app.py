#!/usr/bin/env python3
"""Flask web application with proper 404 error handling."""

from flask import Flask, jsonify

from hello import greet

app = Flask(__name__)


@app.route("/")
def index():
    """Return a greeting for the root path."""
    return jsonify({"message": greet()})


@app.route("/greet/<name>")
def greet_name(name: str):
    """Return a greeting for the given name."""
    return jsonify({"message": greet(name)})


@app.errorhandler(404)
def not_found(_error):
    """Return a JSON 404 response for unknown routes."""
    return jsonify({"error": "Not found", "status": 404}), 404


if __name__ == "__main__":
    app.run()
