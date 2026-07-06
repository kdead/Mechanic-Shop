from .extensions import db

# ---------------------------------------------------------------------
# service_mechanics: this is the join table for the Many-to-Many
# relationship between ServiceTicket and Mechanic. It has no model
# class of its own (no extra columns beyond the two FKs), so it's
# defined as a plain db.Table rather than a db.Model.
# ---------------------------------------------------------------------
service_mechanics = db.Table(
    'service_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20))

    # One-to-Many: one customer -> many service tickets
    service_tickets = db.relationship('ServiceTicket', backref='customer')


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    salary = db.Column(db.Float)

    # Many-to-Many: mechanics <-> service tickets, through service_mechanics
    service_tickets = db.relationship(
        'ServiceTicket',
        secondary=service_mechanics,
        backref='mechanics'
    )


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(17), nullable=False)  # Vehicle Identification Number
    service_date = db.Column(db.String(50))
    service_desc = db.Column(db.String(255))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # customer -> comes for free via the backref='customer' above
    # mechanics -> comes for free via the backref='mechanics' above
