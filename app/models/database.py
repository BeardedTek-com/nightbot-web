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