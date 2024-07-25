from app import app
from app.helpers.nightbot import NightBot

nb = NightBot("https://nightbot.newtowncrew.com")

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

@app.route('/oauth/initiate')
def oauth_initiate():
    return nb.authorize()

@app.route('/oauth/token')
def oauth_token():
    return nb.token()