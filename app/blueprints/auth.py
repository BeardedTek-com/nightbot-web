import os
import secrets
import requests


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
    return redirect(url_for('nightbot.index').replace('http://','https://'))

@auth.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index').replace('http://','https://'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    logs.info(f"##### PROVIDER_DATA #####: {provider_data}")
    
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
    logs.info(f"##### Querystring #####:{qs}")

    return redirect(provider_data['authorize_url'] + '?' + qs)

@auth.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.index').replace('http://','https://'))
    
    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    logs.info(f"##### PROVIDER_DATA #####: {provider_data}")
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
    logs.info(f"##### provider_data #####:\n {provider_data}")
    email = provider_data['userinfo']['email'](response.json())
    logs.info(f"##### email #####:\n {email}")
    logs.info(f"##### Users #####:\n {Users}")

    # Find or create the user in the database
    user = db.session.scalar(db.select(Users).where(Users.email == email))
    if user is None:
        user = Users(email=email, username=email)
        db.session.add(user)
        db.session.commit()
    
    # Log the user in
    login_user(user)
    return redirect(url_for('nightbot.index').replace('http://','https://'))

@auth.route('/user')
@login_required
def view_user():
    return render_template('user.html')

@auth.route('/user/edit')
@login_required
def edit_user():
    return render_template('user_form.html')