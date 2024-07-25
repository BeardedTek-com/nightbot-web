from flask import Flask, redirect, request, jsonify, g
import requests
import json
from app import config
class Auth:
    def __init__(self, app_url):
        self.base_url = "https://api.nightbot.tv"
        self.authorize_path = "/oauth2/authorize"
        self.authorize_url = f"{self.base_url}{self.authorize_path}"
        self.token_path = "/oauth2/token"
        self.token_url = f"{self.base_url}{self.token_path}"
        self.client_id = "84c9ff8165a03c0b5e7b65a9bb3b7e1e"
        self.client_secret = "4197b54c7d9b028956a457cef2ffbd4ed4f412f0bd86c718e57997bc91bf939c"
        self.response_type = "code"
        self.redirect_uri = f"https://nightbot.newtowncrew.com/oauth/token"
        self.scope = "channel"
        self.code = ""
        self.token = {}
        if self.client_id != "" and self.client_secret != "":
            self.ready = True
        else:
            self.ready = False
    
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
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": self.code,
                "grant_type": "authorization_code"
            }
            x = requests.post(self.token_url, data = data)

            self.token = json.loads(x.text)
            if "access_token" in self.token:
                 config['bearer']= self.token["access_token"]
        else:
            return jsonify("ERROR: NO TOKEN")

class API:
    def __init__(self):
        if 'bearer' in config:
            self.api_base_url = "https://api.nightbot.tv/1"
            self.headers = {
                "Authorization": f"Bearer {g.bearer}"
            }
            self.api_ready = True
        else:
            self.api_ready = False
    def get_me(self):
        if self.api_ready:
            api_result = requests.get(
                f"{self.api_base_url}/me",
                headers = self.headers
                )
            return jsonify(api_result.text)
        else:
            return redirect('/', code=302)