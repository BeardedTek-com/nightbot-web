from flask import Flask, redirect, request
import requests

class NightBot:
    def __init__(self, app_url):
        self.base_url = "https://api.nightbot.tv"
        self.authorize_path = "/oauth2/autorize"
        self.authorize_url = f"{self.base_url}{self.authorize_path}"
        self.token_path = "/oauth2/token"
        self.token_url = f"{self.base_url}{self.token_path}"
        self.client_id = "84c9ff8165a03c0b5e7b65a9bb3b7e1e"
        self.client_secret = "95d0895354011ee410a12e261cf2c9bf2a95d228eb71ef1076a1a288a8859e22"
        self.response_type = "code"
        self.redirect_uri = f"https://{app_url}/oauth/token"
        self.scope = "channel channel_send commands commands_default regulars song_requests song_requests_queue song_requests_playlist spam_protection subscribers timers"
        self.token = ""
        if self.client_id != "" and self.client_secret != "":
            self.ready = True
        else:
            self.ready = False
    
    def authorize(self):
        if self.ready:
            print("AUTHORIZE READY")
            redirect(f"{self.authorize_url}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={self.scope}", code=302)
        else:
            print("AUTHORIZE NOT READY")
            redirect("/config", code=302)

    def get_token(self):
        if "token" in request.args:
            self.token = request.args['token']
            return self.token
        else:
            return "ERROR: NO TOKEN"
