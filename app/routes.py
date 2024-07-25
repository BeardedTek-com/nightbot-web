from app import app
import app.helpers.nightbot as NightBot
from app.helpers.home import Home

# NightBot OAuth2
nb_auth = NightBot.Auth("https://nightbot.newtowncrew.com")

# NightBot API
nb_api = NightBot.API()

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
    return nb_auth.authorize()

@app.route('/oauth/token')
def oauth_token():
    return nb_auth.get_token()


# API Routes
@app.route('/get/me')
def get_me():
    return nb_api.get_me()