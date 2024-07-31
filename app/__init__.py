import logging
from flask import Flask

app = Flask(__name__)

logs = logging.getlogger('werkzeug')
data_flask_log = logging.FileHandler('/data/flask.log')
logs.addHandler(data_flask_log)

config = {}

from app import routes