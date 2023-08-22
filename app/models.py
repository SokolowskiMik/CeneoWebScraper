from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String, unique=True, nullable=False )
    opinions_num = db.Column(db.Integer)
    pros = db.Column(db.Integer)
    cons = db.Column(db.Integer)
    mean_score = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    opinions = db.relationship('Opinion')

class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opinion_id = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    recommendation = db.Column(db.String)
    score = db.Column(db.Integer)
    purchased = db.Column(db.String)
    published_at = db.Column(db.String)
    purchased_at = db.Column(db.String)
    thumbs_up = db.Column(db.Integer)
    thumbs_down = db.Column(db.Integer)
    content = db.Column(db.String)
    pros = db.Column(db.Integer)
    cons = db.Column(db.Integer)
    product_code = db.Column(db.String, db.ForeignKey('product.product_code'))