import os
import secrets
import requests

from validators import url as validate_url
from time import ctime, time
from urllib.parse import urlencode
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, redirect, url_for, render_template, flash, abort, \
    session, current_app, request

from app import db
from app import login
from app import logs
from app.models.database import Users
from app.helpers.modpipe import get_form_data

auth = Blueprint('auth', __name__)

@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))

@auth.route('/')
def index():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('modpipe.index').replace('http://','https://'))

@auth.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index').replace('http://','https://'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    logs.debug(f"##### PROVIDER_DATA #####: {provider_data}")
    
    if provider_data is None:
        abort(404)

    # Generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # Create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('auth.oauth2_callback', provider=provider, _external=True).replace('http://','https://'),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })
    logs.debug(f"##### Querystring #####:{qs}")

    return redirect(provider_data['authorize_url'] + '?' + qs)

@auth.route('/callback/<provider>')
def oauth2_callback(provider, new_user=False):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index').replace('http://','https://'))
    
    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    logs.debug(f"##### PROVIDER_DATA #####: {provider_data}")
    if provider_data is None:
        abort(404)
    
    # If there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in requests.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('auth.index').replace('http://','https://'))
    
    # Make sure the state parameter matches the one we created
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)
    
    # Make sure the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # Exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('auth.oauth2_callback', provider=provider, _external=True).replace('http://','https://'),
        },
        headers={'Accept': 'application/json'}
    )
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)
    
    # Use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
            'Authorization': 'Bearer ' +oauth2_token,
            'Accept': 'application/json',
        })
    if response.status_code != 200:
        abort(401)
    logs.debug(f"##### provider_data #####:\n {provider_data}")
    email = provider_data['userinfo']['email'](response.json())
    logs.debug(f"##### email #####:\n {email}")
    logs.debug(f"##### Users #####:\n {Users}")

    # Find or create the user in the database
    user = db.session.scalar(db.select(Users).where(Users.email == email))
    if user is None:
        user = Users(email=email)
        new_user = True
    user.last_used = int(time())
    db.session.add(user)
    db.session.commit()

    # Log the user in
    login_user(user)

    # Onboard User and allow them to edit their profile
    user = db.session.scalar(db.select(Users).where(Users.email == email))
    if new_user:
        return render_template('onboarding.html',user=user)
    else:
        return redirect(url_for('modpipe.index').replace('http://','https://'))


@auth.route('/user')
@login_required
def view_user():
    return render_template('user.html')

@auth.route('/user/edit', methods=['GET'])
@login_required
def edit_user():
    user = db.session.scalar(db.select(Users).where(Users.id == current_user.id))
    return render_template('user_form.html', user=user)

@auth.route('/user/update', methods=['POST'])
@login_required
def edit_user_POST():
    fields = ['type','id','groups','username','email','admin','display','avatar','bio', 'onboarding']
    form_data = get_form_data(fields)

    user = db.session.scalar(db.select(Users).where(Users.email == form_data['email']))
    display_change_date = int(time()) - 2592000
    user.username = f"""{form_data['username']}"""
    user.display = f"""{form_data['display']}"""
    user.avatar = f"""{form_data['avatar']}"""
    user.admin = f"""{form_data['admin']}"""
    user.bio = f"""{form_data['bio']}"""

    db.session.commit()
    if form_data['type'] == "onboarding":
        return redirect(f"{url_for('modpipe.index').replace('http://','https://')}?welcome")
    return redirect(url_for('auth.edit_user').replace('http://','https://'))