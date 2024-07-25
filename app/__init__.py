from flask import Flask

app = Flask(__name__)

config = {}

from app import routes