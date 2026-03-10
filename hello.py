#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
