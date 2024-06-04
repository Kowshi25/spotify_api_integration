from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

app = Flask(__name__)

app.secret_key = "secret_key"
app.config["SESSION_COOKIE_NAME"] = "Vibe it cookie"
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/getPlaylist')
def getPlaylist():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info["access_token"])
    return sp.current_user_saved_albums(limit=10, offset=0)['items'][0]

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = time.time()
    is_expired = token_info["expires_at"] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

    return token_info
@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getPlaylist', _external=True))

client_id = 'id'
client_secret = 'secret'


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='04aa54106aea4c298e0bff75629acb64',
        client_secret='7b753b35e9f2475f9980d27e4dd692c5',
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read'
    )
