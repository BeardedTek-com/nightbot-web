from flask import redirect
import os

api_endpoints = {
    "me": "/get/me"
}

class Home:
    def index(self):
        if "NIGHTBOT_BEARER" not in os.environ:
            return "<a href='/oauth/initiate'>LOGIN</a>"
        else:
            return "Already Authorized"