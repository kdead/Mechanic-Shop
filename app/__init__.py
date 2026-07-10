from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db, ma, limiter, cache

SWAGGER_URL = '/api/docs'          # URL for exposing Swagger UI (no trailing '/')
API_URL = '/static/swagger.yaml'   # Where the OpenAPI spec is served from

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API"
    }
)


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    from .blueprints.customer import customer_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp
    from .blueprints.inventory import inventory_bp

    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
