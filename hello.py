#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"message": "Hello World"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "status": 404}), 404


if __name__ == "__main__":
    app.run(debug=False)
