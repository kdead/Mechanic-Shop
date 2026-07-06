from flask import request, jsonify
from app.extensions import db
from app.models import Customer
from . import customer_bp
from .schemas import customer_schema, customers_schema


@customer_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer = customer_schema.load(request.json)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers), 200


@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200


@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        updated_customer = customer_schema.load(request.json, instance=customer, partial=True)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return customer_schema.jsonify(updated_customer), 200


@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted"}), 200
