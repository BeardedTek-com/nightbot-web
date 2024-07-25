import os

api_endpoints = {
    "me": "/get/me"
}

class Home:
    def index(self):
        if "NIGHTBOT_BEARER" not in os.environ:
            self.login()
        else:
            self.api_list()
    def login(self):
        return "<a href='/oauth/initiate'>LOGIN</a>"
    
    def api_list(self):
        output = ""
        for endpoint in api_endpoints:
            output += f"<a href='{api_endpoints[endpoint]}'>{endpoint}</a></br>"
        if output == "":
            return "No Endpoints configured"
        else:
            return output