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
@app.route('/api')
def api():
    return "Default API Route"

@app.route('/1', defaults={'path1': None,'path2':None,'path3':None})
@app.route('/1/<path1>', defaults={'path2':None,'path3':None})
@app.route('/1/<path1/<path2>',defaults={'path3':None})
@app.route('/1/<path1/<path2>/<path3>')
def api_catchall(path1,path2,path3):
    path = f"/1"
    path = f"{path}/{path1}" if path1 else path
    path = f"{path}/{path2}" if path2 else path
    path = f"{path}/{path3}" if path3 else path
    return f"You are looking for {path}"


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
        param = id,
        data = None
    )