#!/usr/bin/env python3
"""Flask REST API exposing user profile CRUD endpoints."""

from flask import Flask, jsonify, request

from user_profile import (
    DuplicateUsernameError,
    InvalidProfileDataError,
    UserNotFoundError,
    UserProfileStore,
)

app = Flask(__name__)
store = UserProfileStore()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/profiles", methods=["GET"])
def list_profiles():
    """Return all user profiles."""
    return jsonify({"profiles": [p.to_dict() for p in store.list_all()]})


@app.route("/profiles", methods=["POST"])
def create_profile():
    """Create a new user profile."""
    data = request.get_json(silent=True) or {}
    try:
        profile = store.create(
            username=data.get("username", ""),
            email=data.get("email", ""),
            bio=data.get("bio", ""),
            avatar_url=data.get("avatar_url", ""),
        )
    except DuplicateUsernameError as exc:
        return jsonify({"error": str(exc)}), 409
    except InvalidProfileDataError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(profile.to_dict()), 201


@app.route("/profiles/<int:user_id>", methods=["GET"])
def get_profile(user_id: int):
    """Return the profile with the given ID."""
    try:
        profile = store.get(user_id)
    except UserNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify(profile.to_dict())


@app.route("/profiles/<int:user_id>", methods=["PUT"])
def update_profile(user_id: int):
    """Update an existing profile."""
    data = request.get_json(silent=True) or {}
    try:
        profile = store.update(
            user_id,
            username=data.get("username"),
            email=data.get("email"),
            bio=data.get("bio"),
            avatar_url=data.get("avatar_url"),
        )
    except UserNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except DuplicateUsernameError as exc:
        return jsonify({"error": str(exc)}), 409
    except InvalidProfileDataError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(profile.to_dict())


@app.route("/profiles/<int:user_id>", methods=["DELETE"])
def delete_profile(user_id: int):
    """Delete the profile with the given ID."""
    try:
        store.delete(user_id)
    except UserNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify({"deleted": user_id})


@app.errorhandler(404)
def not_found(error):
    """Return a JSON 404 response for unmatched routes."""
    return jsonify({"error": "Not found", "message": str(error)}), 404


if __name__ == "__main__":
    app.run(debug=False)
