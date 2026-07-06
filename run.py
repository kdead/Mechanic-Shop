from app import create_app
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables from your models if they don't exist yet
    app.run(debug=True)
