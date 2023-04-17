#For .env
from dotenv import load_dotenv
import os

import base64
from flask import Flask, redirect, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

#credentials for Spotify API
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')
    #return '<a href="/login">Log in with Spotify</a>'

# Login route
@app.route('/login')
def login():
    # Redirect the user to the Spotify login page
    scope = 'playlist-modify-public'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope
    }
    url = f'{AUTH_URL}?client_id={params["client_id"]}&response_type={params["response_type"]}&redirect_uri={params["redirect_uri"]}&scope={params["scope"]}'
    return redirect(url)

# Callback route
@app.route('/callback')
def callback():
    # Exchange the authorization code for an access token
    code = request.args.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']
    print(f"access_token: {access_token}")
    print(f"refresh_token: {refresh_token}")

    # Create a new playlist for the user
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_id = response.json()['id']
    print(f"user_id: {user_id}")
    data = {
        'name': 'My New Playlist',
        'description': 'A new playlist created with the Spotify API',
        'public': False
    }
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code != 201:
        print('Could not create playlist')
        return 'Could not create playlist'
    playlist_id = response.json()['id']

    #return f'New playlist created with ID' 
    return f'New playlist created with ID {playlist_id}'

if __name__ == "__main__":
    app.run(debug=True)