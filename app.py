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


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)