from flask import Blueprint

customer_bp = Blueprint('customer_bp', __name__)

# Import routes AFTER the blueprint is created, so routes.py can
# import customer_bp from this file without a circular import.
from . import routes
