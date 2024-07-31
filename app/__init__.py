import logging
from flask import Flask
from flask.logging import default_handler

app = Flask(__name__)

# Setup logging
logs = logging.getLogger('werkzeug')
# Log to '/data/flask.log'
data_flask_log = logging.FileHandler('/data/flask.log')
logs.addHandler(data_flask_log)
# Log to 'stderr'
logs.addHandler(default_handler)



config = {}

from app import routes