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