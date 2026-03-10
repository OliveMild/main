#!/usr/bin/env python3
"""Simple Flask web application."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Return a greeting message."""
    return jsonify({"message": "Hello World"})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404


if __name__ == "__main__":
    import os
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
