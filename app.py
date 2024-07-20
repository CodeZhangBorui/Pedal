"""Main application of Pedal app."""

# Import libs
import os
import json

from flask import Flask
from flask_apscheduler import APScheduler

# Import routes
from routes.pages import pages
from routes.clients import clients

# Load config from json file
with open("config.json", encoding='utf-8') as file:
    config = json.load(file)

# Initalize Flask app
app = Flask(__name__)
if config["flask"]["debug"]:
    app.debug = True
app.secret_key = os.urandom(24)

# Register routes
app.register_blueprint(pages)
app.register_blueprint(clients)

# Register scheduler

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0')