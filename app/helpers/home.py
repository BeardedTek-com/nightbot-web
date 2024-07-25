from flask import redirect
import os
from app import config

api_endpoints = {
    "me": "/get/me"
}

class Home:
    def index(self):
        if 'bearer' in config:
            return "Already Authorized"
        else:
            return "<a href='/oauth/initiate'>LOGIN</a>"