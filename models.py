from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy(metadata = metadata)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(256), nullable = False)
    password = db.Column(db.String(40), nullable = False)
    phone_number = db.Column(db.String(10), nullable = False)

    order = db.relationship("Order", back_populates = "user", cascade = "all, delete-orphan")

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    items_ordered = db.Column(db.String(128), nullable = False)
    total_amount = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(40), nullable = False)
    date_ordered = db.Column(db.DateTime, nullable = False)

    user = db.relationship("User", back_populates = "order")