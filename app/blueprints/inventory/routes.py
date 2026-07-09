from flask import request, jsonify
from app.extensions import db
from app.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema


@inventory_bp.route('/', methods=['POST'])
def create_part():
    try:
        part = inventory_schema.load(request.json)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201


@inventory_bp.route('/', methods=['GET'])
def get_parts():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts), 200


@inventory_bp.route('/<int:id>', methods=['GET'])
def get_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    return inventory_schema.jsonify(part), 200


@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    try:
        updated_part = inventory_schema.load(request.json, instance=part, partial=True)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return inventory_schema.jsonify(updated_part), 200


@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {id} deleted"}), 200