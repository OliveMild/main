from flask import Flask, jsonify

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found", message=str(e)), 404


@app.route("/items/<int:item_id>")
def get_item(item_id):
    # Simulate a database of items
    items = {1: "apple", 2: "banana", 3: "cherry"}
    if item_id not in items:
        return jsonify(error="Item not found", item_id=item_id), 404
    return jsonify(item_id=item_id, name=items[item_id])


if __name__ == "__main__":
    app.run()
