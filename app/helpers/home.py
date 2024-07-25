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
            return self.api_list()

    def api_list(self):
        output = ""
        for endpoint in api_endpoints:
            output += f"<a href='{api_endpoints[endpoint]}'>{endpoint}</a></br>"
        if output == "":
            return "No Endpoints configured"
        else:
            return output