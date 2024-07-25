from app import app
from app.helpers.nightbot import NightBot
from flask import request

# NightBot OAuth2
nb = NightBot("https://nightbot.newtowncrew.com")

@app.route('/')
@app.route('/index')
def index():
    return nb.index()

@app.route('/config')
def config():
    return "Config Page will go here"


# OAuth Routes
@app.route('/oauth/initiate')
def oauth_initiate():
    return nb.authorize()

@app.route('/oauth/token')
def oauth_token():
    return nb.get_token()


# API Routes
@app.route('/get/me')
def get_me():
    return nb.get_me()
@app.route('/api/channel/send')
def channel_send():
    message = request.args.get('message') if 'message' in request.args else None
    return nb.channel_send(message=message)