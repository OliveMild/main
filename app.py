#!/usr/bin/env python3
"""Simple Flask web application."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Home route."""
    return jsonify({"message": "Hello World"})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "Not Found", "message": str(error)}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)
