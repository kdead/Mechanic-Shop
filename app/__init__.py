from flask import Flask
from .extensions import db, ma


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    # Imported here (inside the factory) so the blueprints are only
    # wired up once the app + extensions already exist.
    from .blueprints.customer import customer_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp

    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    return app
