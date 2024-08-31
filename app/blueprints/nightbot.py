import os
import secrets
import requests

from urllib.parse import urlencode
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from flask import Blueprint, redirect, url_for, render_template, flash, abort, \
                  session, current_app, request

from app import db
from app import login
from app import logs
from app.models.database import Users
from app.models.database import NightBot
from app.helpers.nightbot import NightBot
from app.helpers.validate import is_url
from app import app

with app.app_context():
    nightbot_config = current_app.config['NIGHTBOT_OAUTH'] if 'NIGHTBOT_OAUTH' in current_app.config else None



nb = NightBot()

nightbot = Blueprint('nightbot', __name__)

@nightbot.route('/')
def index():
    return render_template('main.html')

@nightbot.route('/config', methods=['GET'])
@login_required
def config():
    return render_template('config.html')

@nightbot.route('/config', methods=['POST'])
@login_required
def config_save():
    pass

@nightbot.route('/authorize')
@login_required
def oauth_authorize():
    return nb.oauth2_authorize(client_id="")

@nightbot.route('/callback')
@login_required
def oauth_callback():
    return nb.oauth2_callback(client_id="",client_secret="")