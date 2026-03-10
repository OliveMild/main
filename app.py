#!/usr/bin/env python3
"""Flask application with custom 404 error handling."""

from flask import Flask, jsonify

app = Flask(__name__)

# In-memory items store for demonstration
ITEMS = {
    1: {"name": "Widget", "price": 9.99},
    2: {"name": "Gadget", "price": 24.99},
}


@app.errorhandler(404)
def not_found(error):
    """Return a JSON 404 response instead of the default HTML page."""
    return jsonify({"error": "Not found", "message": str(error)}), 404


@app.route("/")
def index():
    """Return a simple greeting."""
    return jsonify({"message": "Hello World"})


@app.route("/items/<int:item_id>")
def get_item(item_id):
    """Return an item by ID, or a JSON 404 if not found."""
    item = ITEMS.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found", "item_id": item_id}), 404
    return jsonify({"item_id": item_id, **item})


if __name__ == "__main__":
    app.run()
