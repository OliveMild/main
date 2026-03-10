from flask import Flask, jsonify
import os
import hello

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": hello.greet()})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "status": 404}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed", "status": 405}), 405


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
