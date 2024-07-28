from flask import request

from app import app
from app.helpers.nightbot import NightBot
from app.models.api import API as api_model
api = api_model()

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
    return nb.oauth2_authorize()

@app.route('/oauth/token')
def oauth_token():
    return nb.oauth2_token()


# API Routes
@app.route('/api/me')
def get_me():
    return nb.api_send(
        api.me,
        data = None
    )

@app.route('/api/channel/send')
def channel_send():
    return nb.channel_send()

@app.route('/api/channel/send/<file>')
def channel_send_file(file):
    return nb.channel_send_from_file(file)



@app.route('/api/commands/get')
def commands_get_all():
    return nb.api_send(
        api.custom_commands_get_all,
        data = None
    )

@app.route('/api/commands/get/<id>')
def commands_get_by_id(id):
    return nb.api_send(
        api.custom_command_get,
        data = None
    )