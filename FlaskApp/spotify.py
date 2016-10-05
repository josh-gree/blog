import os
import base64
import requests
import json
import spotipy

from mongoengine import connect
from flask import url_for, redirect, request, render_template
from urllib.parse import quote
from FlaskApp import app

from FlaskApp.helpers import stringToBase64
from FlaskApp.model import SpotifyAuth

from FlaskApp.NOVCONT import *

db = connect('blog_posts')

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

REDIRECT_URI = "http://josh-gree.me/auth/callback"
SCOPE = "playlist-read-private playlist-read-collaborative user-library-read user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

@app.route("/spotify")
def sp():
    return render_template("spotify.html")

@app.route("/auth")
def auth():
    url_args = "&".join(["{}={}".format(key,quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/auth/callback")
def auth_callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = stringToBase64("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).decode("ascii")
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]

    sp = spotipy.Spotify(auth=access_token)
    user = sp.current_user()
    username = user['id']
    name = user['display_name']
    if not SpotifyAuth.objects(username=username):
        SpotifyAuth(username=username,access_token=access_token,refresh_token=refresh_token).save()

    name = username if name is None else name


    return render_template('thanks.html', name = name)
