from flask import Flask, jsonify

app = Flask(__name__)

# In-memory "database" of items
ITEMS = {
    1: {"name": "Widget"},
    2: {"name": "Gadget"},
}


@app.route("/items/<int:item_id>")
def get_item(item_id):
    item = ITEMS.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found", "item_id": item_id}), 404
    return jsonify({"item_id": item_id, **item})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "message": str(e)}), 404


if __name__ == "__main__":
    app.run()
