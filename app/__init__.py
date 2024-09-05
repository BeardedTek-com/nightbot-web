import os
import logging
from time import ctime
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

# Setup Database
db = SQLAlchemy(app)

# Login Manager
login = LoginManager(app)
login.login_view = 'index'

# Setup logging
logs = logging.getLogger('werkzeug')
# Log to '/data/flask.log'
data_flask_log = logging.FileHandler('/data/flask.log')
logs.addHandler(data_flask_log)
# Log to 'stderr'
logs.addHandler(default_handler)

# Routes
from app import routes
from app.blueprints.auth import auth as auth_blueprint
from app.blueprints.modpipe import modpipe as modpipe_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(modpipe_blueprint, url_prefix='/modpipe')


from app.models import database
with app.app_context():
    db.create_all()

@app.template_filter('ctime')
def timectime(s):
    return ctime(s)