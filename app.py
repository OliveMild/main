#!/usr/bin/env python3
"""Flask web application exposing the greeting functionality over HTTP."""

from flask import Flask, jsonify

from hello import greet

app = Flask(__name__)


@app.route("/")
def index():
    """Return a JSON greeting for the world."""
    return jsonify({"message": greet()})


@app.route("/greet/<name>")
def greet_name(name: str):
    """Return a JSON greeting for the given name."""
    return jsonify({"message": greet(name)})


@app.errorhandler(404)
def not_found(error):
    """Return a JSON 404 response instead of the default HTML page."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run()
