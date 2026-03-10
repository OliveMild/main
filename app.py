#!/usr/bin/env python3
"""Simple Flask web application with proper 404 error handling."""

import os

from flask import Flask, jsonify

app = Flask(__name__)

# In-memory item store for demonstration purposes
_ITEMS = {
    1: {"id": 1, "name": "Widget", "description": "A useful widget"},
    2: {"id": 2, "name": "Gadget", "description": "A handy gadget"},
}


@app.route("/")
def index():
    """Return a welcome message."""
    return jsonify({"message": "Welcome to the application", "status": "ok"})


@app.route("/items")
def list_items():
    """Return all available items."""
    return jsonify({"items": list(_ITEMS.values())})


@app.route("/items/<int:item_id>")
def get_item(item_id):
    """Return the item with the given ID, or 404 if not found."""
    item = _ITEMS.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found", "item_id": item_id}), 404
    return jsonify(item)


@app.errorhandler(404)
def not_found(error):
    """Return a JSON 404 response for any unmatched route."""
    return jsonify({"error": "Not found", "message": str(error)}), 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False") == "True")
