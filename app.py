#!/usr/bin/env python3
import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Hello World"}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error), "status": 404}), 404


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
