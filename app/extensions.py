from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

db = SQLAlchemy()
ma = Marshmallow()

# key_func=get_remote_address means limits are tracked per visitor IP.
limiter = Limiter(key_func=get_remote_address)

# Simple in-memory cache 
cache = Cache()