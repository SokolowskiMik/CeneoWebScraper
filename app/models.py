from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))


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