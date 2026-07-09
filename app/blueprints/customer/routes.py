from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, limiter
from app.models import Customer
from app.auth import encode_token, token_required
from . import customer_bp
from .schemas import customer_schema, customers_schema, login_schema


@customer_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer = customer_schema.load(request.json)
    except Exception as e:
        return jsonify(e.messages), 400

    # Never store the raw password - hash it before saving.
    customer.password = generate_password_hash(customer.password)

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


# Pagination: /customers/?page=1&per_page=10
@customer_bp.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "customers": customers_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200


@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200


@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "You can only update your own account"}), 403

    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        updated_customer = customer_schema.load(request.json, instance=customer, partial=True)
    except Exception as e:
        return jsonify(e.messages), 400

    if request.json.get('password'):
        updated_customer.password = generate_password_hash(request.json['password'])

    db.session.commit()
    return customer_schema.jsonify(updated_customer), 200


@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "You can only delete your own account"}), 403

    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted"}), 200


@customer_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        data = login_schema.load(request.json)
    except Exception as e:
        return jsonify(e.messages), 400

    customer = Customer.query.filter_by(email=data['email']).first()

    if not customer or not check_password_hash(customer.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(customer.id)
    return jsonify({"token": token}), 200