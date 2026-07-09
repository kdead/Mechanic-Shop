from .extensions import db

# ---------------------------------------------------------------------
# service_mechanics: join table for Many-to-Many between
# ServiceTicket and Mechanic.
# ---------------------------------------------------------------------
service_mechanics = db.Table(
    'service_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

# ---------------------------------------------------------------------
# ticket_inventory: join table for Many-to-Many between
# ServiceTicket and Inventory (a ticket can use many parts, and the
# same part can be used across many tickets).
# ---------------------------------------------------------------------
ticket_inventory = db.Table(
    'ticket_inventory',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    # Added for Lesson 7 (Token Authentication) - stores a HASHED password,
    # never plain text. See customer routes.py for the hashing step.
    password = db.Column(db.String(255), nullable=False)

    service_tickets = db.relationship('ServiceTicket', backref='customer')


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    salary = db.Column(db.Float)

    service_tickets = db.relationship(
        'ServiceTicket',
        secondary=service_mechanics,
        backref='mechanics'
    )


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.String(50))
    service_desc = db.Column(db.String(255))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    parts = db.relationship(
        'Inventory',
        secondary=ticket_inventory,
        backref='service_tickets'
    )


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)