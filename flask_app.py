from app import create_app
from app.extensions import db

app = create_app('config.ProductionConfig')

with app.app_context():
    db.create_all()  # creates tables on the hosted Postgres db if they don't exist yet

