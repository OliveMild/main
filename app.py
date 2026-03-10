#!/usr/bin/env python3
from flask import Flask, jsonify

from hello import greet

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": greet()})


@app.route("/greet/<name>")
def greet_name(name):
    return jsonify({"message": greet(name)})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run()
