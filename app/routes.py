from flask import request

from app import app
from app.helpers.nightbot import NightBot
from app.models.api import API as api_model
api = api_model()

# NightBot OAuth2
nb = NightBot("https://nightbot.newtowncrew.com",
              client_id="84c9ff8165a03c0b5e7b65a9bb3b7e1e",
              client_secret="95d68d5540b2bb376f4452990052b3dace1573a8b6db86eddcad8584c103e6c3",
              scope = "channel \
                       channel_send \
                       commands \
                       commands_default \
                       regulars \
                       subscribers \
                       song_requests \
                       song_requests_queue \
                       song_requests_playlist \
                       spam_protection \
                       timers",
              debug=True)

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

# Default API Route
@app.route('/api', defaults={'category': None,'command':None,'cmd_var':None})
@app.route('/api/<category>', defaults={'command':None,'cmd_var':None})
@app.route('/api/<category>/<command>',defaults={'cmd_var':None})
@app.route('/api/<category>/<command>/<cmd_var>')
def api_catchall(category,command,cmd_var):
    # Channel
    if category == "channel":
        if command == "send":
            if cmd_var:
                nb.channel_send_from_file(cmd_var)
            else:
                nb.channel_send()
    
    # Commands
    if category == "commands":
        if command == "get":
            if cmd_var:
                return nb.api_send(
                    api.custom_command_get,
                    param = cmd_var,
                    data = None
                )
            else:
                return nb.api_send(
                    api.custom_commands_get_all,
                    data = None
                )
    # Me
    if category == "me":
        return nb.api_send(
            api.me,
            data = None
        )
        
    else:
        path = f"/api"
        for value in [category,command,cmd_var]:
            path = f"{path}/{value}" if value else path
        return {"error" : "not implemented"}
