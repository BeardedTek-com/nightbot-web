from app import db
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    groups = db.Column(JSON)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    admin = db.Column(db.String(10))
    display = db.Column(db.String(64))
    avatar = db.Column(db.String(1024))
    bio = db.Column(db.String(4096))
    last_used = db.Column(db.Integer())
    display_modified = db.Column(db.Integer())

class Groups(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    owner = db.Column(db.Integer())
    name = db.Column(db.String(64))
    last_used = db.Column(db.Integer())

class NightBot(db.Model):
    __tablename__ = 'nightbot'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer())
    name = db.Column(db.String(64))
    displayName = db.Column(db.String(64))
    avatar = db.Column(db.String(2048))
    admin = db.Column(db.Boolean(), default=False)
    client_id = db.Column(db.String(32))
    client_secret = db.Column(db.String(64))
    last_used = db.Column(db.Integer())

class Twitch(db.Model):
    __tablename__ = 'twitch'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer())
    name = db.Column(db.String(64))
    displayName = db.Column(db.String(64))
    avatar = db.Column(db.String(2048))
    admin = db.Column(db.Boolean(), default=False)
    client_id = db.Column(db.String(32))
    client_secret = db.Column(db.String(64))
    last_used = db.Column(db.Integer())

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer())
    users = db.Column(JSON)
    groups = db.Column(JSON)
    name = db.Column(db.String(64))
    message = db.Column(db.String(6000))
    last_used = db.Column(db.Integer())

class Commands(db.Model):
    __tablename__ = 'commands'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer())
    users = db.Column(JSON)
    groups = db.Column(JSON)
    name = db.Column(db.String(64))
    type = db.Column(db.String(32))
    command = db.Column(db.String(4096))
    short_description = db.Column(db.String(64))
    long_description = db.Column(db.String(512))
    timeout = db.Column(db.Integer())
    image_url = db.Column(db.String(1024))
    last_used = db.Column(db.Integer())

