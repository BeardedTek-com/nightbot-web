from app import db
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    admin = db.Column(db.Boolean(), default=False)
    display = db.Column(db.String(64))

class NightBot(db.Model):
    __tablename__ = 'nightbot'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    name = db.Column(db.String(64))
    displayName = db.Column(db.String(64))
    avatar = db.Column(db.String(2048))
    admin = db.Column(db.Boolean(), default=False)
    client_id = db.Column(db.String(32))
    client_secret = db.Column(db.String(64))
