import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD')


class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/mechanic_shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 60


import os

# python-dotenv is only used for local development, to load a .env file.
# It's intentionally NOT in requirements.txt so it isn't a hard dependency
# in production (Render sets real environment variables directly, no .env
# file involved). Import it defensively so the app still starts if it's
# not installed.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_PASSWORD = os.getenv('DB_PASSWORD')


class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/mechanic_shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 60


class ProductionConfig:
    """Used by flask_app.py when deployed on Render. Points at the hosted
    Postgres database and reads the secret key from real environment
    variables set in the Render dashboard - never from a .env file."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super secret secrets'

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 60


class TestingConfig:
    """Used by tests/ - runs against a throwaway SQLite file instead of the
    real MySQL database, so running the test suite never touches production
    or development data."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True

    SECRET_KEY = 'test-secret-key'

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 60

    # Disable rate limiting during tests so the login-related
    # test cases in test_customer.py can't get 429'd by earlier tests.
    RATELIMIT_ENABLED = False