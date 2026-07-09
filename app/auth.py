from functools import wraps
from datetime import datetime, timedelta, timezone

from flask import request, jsonify, current_app
from jose import jwt, JWTError


def encode_token(customer_id):
    """Builds a JWT that identifies a specific customer, valid for 1 day."""
    payload = {
        'sub': str(customer_id),               # who the token belongs to
        'iat': datetime.now(timezone.utc),     # issued-at time
        'exp': datetime.now(timezone.utc) + timedelta(days=1)  # expiration
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    """
    Decorator for routes that require a logged-in customer.
    Expects a header:  Authorization: Bearer <token>
    On success, passes customer_id as the first argument to the route.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({"error": "Authorization header must be: Bearer <token>"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            customer_id = int(data['sub'])
        except JWTError:
            return jsonify({"error": "Token is invalid or expired"}), 401

        return f(customer_id, *args, **kwargs)

    return decorated