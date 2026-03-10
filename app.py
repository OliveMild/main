#!/usr/bin/env python3

import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Hello World"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug)
