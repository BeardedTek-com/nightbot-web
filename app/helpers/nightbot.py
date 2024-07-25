from flask import Flask, redirect, request, jsonify, g
import requests
import json
class NightBot:
    def __init__(self, app_url):
        self.base_url = "https://api.nightbot.tv"
        self.api_base_url = f"{self.base_url}/1"
        self.authorize_path = "/oauth2/authorize"
        self.authorize_url = f"{self.base_url}{self.authorize_path}"
        self.token_path = "/oauth2/token"
        self.token_url = f"{self.base_url}{self.token_path}"
        self.client_id = "84c9ff8165a03c0b5e7b65a9bb3b7e1e"
        self.client_secret = "4197b54c7d9b028956a457cef2ffbd4ed4f412f0bd86c718e57997bc91bf939c"
        self.response_type = "code"
        self.redirect_uri = f"https://nightbot.newtowncrew.com/oauth/token"
        self.scope = "channel"
        self.code = None
        self.token = {}
        self.bearer = None
        if self.client_id != "" and self.client_secret != "":
            self.ready = True
        else:
            self.ready = False

    def index(self):
        if self.bearer:
            return "Already Authorized"
        else:
            return "<a href='/oauth/initiate'>LOGIN</a>"
        
    def authorize(self):
        if self.ready:
            print("AUTHORIZE READY")
            redirect_url = f"{self.authorize_url}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={self.scope}"
            print(redirect_url)
            return redirect( redirect_url, code=302)
        else:
            print("AUTHORIZE NOT READY")
            return redirect("/config", code=302)

    def get_token(self):
        if "code" in request.args:
            self.code = request.args['code']
            data = {
                "client_id"      : self.client_id,
                "client_secret"  : self.client_secret,
                "code"           : self.code,
                "grant_type"     : "authorization_code"
            }
            x = requests.post(self.token_url, data = data)

            self.token = json.loads(x.text)
            if "access_token" in self.token:
                 self.bearer= self.token["access_token"]
                 self.headers = {
                    "Authorization": f"Bearer {self.bearer}"
                }
            return redirect('/', code=302)
        else:
            return jsonify("ERROR: NO TOKEN")
    def get_me(self):
        if not self.headers:
            return redirect('/', code=302)
        else:
            api_result = requests.get(
                f"{self.api_base_url}/me",
                headers = self.headers
                )
            result_json = json.loads(api_result.text)
            
            return jsonify(result_json)
    
    def channel_send(self,message=None):
        if not self.headers:
            return redirect('/', code=302)
        else:
            if not message:
                message = "This is a test of channel send from NightBot-Web."
            data = {
                "message"        : message
            }
            x = requests.post(
                f"{self.api_base_url}/channel/send",
                data = data,
                headers = self.headers
                )