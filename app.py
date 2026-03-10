"""Flask application exposing user profile endpoints."""

from flask import Flask, jsonify, request

from hello import greet
import user_profile as up

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(up.UserNotFoundError)
def handle_user_not_found(error: up.UserNotFoundError):
    return jsonify({"error": str(error), "status": 404}), 404


@app.errorhandler(up.InvalidProfileDataError)
def handle_invalid_profile(error: up.InvalidProfileDataError):
    return jsonify({"error": str(error), "status": 400}), 400


@app.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Not found", "status": 404}), 404


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return jsonify({"message": greet()})


@app.route("/profiles", methods=["GET"])
def list_profiles():
    return jsonify(up.list_profiles())


@app.route("/profiles", methods=["POST"])
def create_profile():
    body = request.get_json() or {}
    profile = up.create_profile(body.get("name", ""), body.get("email", ""))
    return jsonify(profile), 201


@app.route("/profiles/<int:user_id>", methods=["GET"])
def get_profile(user_id: int):
    return jsonify(up.get_profile(user_id))


@app.route("/profiles/<int:user_id>", methods=["PUT"])
def update_profile(user_id: int):
    body = request.get_json() or {}
    profile = up.update_profile(user_id, body.get("name", ""), body.get("email", ""))
    return jsonify(profile)


@app.route("/profiles/<int:user_id>", methods=["DELETE"])
def delete_profile(user_id: int):
    up.delete_profile(user_id)
    return "", 204


if __name__ == "__main__":
    app.run()
