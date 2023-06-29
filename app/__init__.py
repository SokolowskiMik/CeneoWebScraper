from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfsa123adas235agsdgas2292gulglulgugluioiophjgh9292929abdsbdsabsbd2352780ccbazcnxgkjlguscbsdb'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
db.init_app(app)

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

from app import routes

from .models import Product, Opinion

with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)


