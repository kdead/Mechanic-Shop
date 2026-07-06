from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# These live here (instead of in models.py or __init__.py) so that
# models.py, schemas.py, and app/__init__.py can all import them
# without creating circular imports.
db = SQLAlchemy()
ma = Marshmallow()
