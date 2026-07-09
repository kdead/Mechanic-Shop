from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic, Inventory
from app.auth import token_required
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema


@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket = service_ticket_schema.load(request.json)
    except Exception as e:
        return jsonify(e.messages), 400

    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        return jsonify({"message": "That mechanic is already assigned to this ticket"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} assigned to ticket {ticket_id}"}), 200


@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"message": "That mechanic is not assigned to this ticket"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}"}), 200


@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    data = request.json or {}
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, inventory_id)

    if not ticket or not part:
        return jsonify({"error": "Service ticket or inventory part not found"}), 404

    if part in ticket.parts:
        return jsonify({"message": "That part is already on this ticket"}), 400

    ticket.parts.append(part)
    db.session.commit()
    return jsonify({"message": f"Part {inventory_id} added to ticket {ticket_id}"}), 200
