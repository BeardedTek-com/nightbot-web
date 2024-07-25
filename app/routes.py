from app import app
from app.helpers.nightbot import NightBot
from app.helpers.home import Home

# NightBot OAuth2
nb = NightBot.NightBot("https://nightbot.newtowncrew.com")

# NightBot Index
nb_home = Home()

@app.route('/')
@app.route('/index')
def index():
    return nb_home.index()

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