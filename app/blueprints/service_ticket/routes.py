from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
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

    # Because of the relationship() with secondary=service_mechanics on the
    # Mechanic model, ticket.mechanics behaves like a normal Python list.
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
