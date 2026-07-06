from flask import request, jsonify
from app.extensions import db
from app.models import Mechanic
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic = mechanic_schema.load(request.json)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        updated_mechanic = mechanic_schema.load(request.json, instance=mechanic, partial=True)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(updated_mechanic), 200


@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200
