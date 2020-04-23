# main.py ---
#
# Filename: main.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:47:03 2020 (+0200)
# Last-Updated: Thu Apr 23 17:56:23 2020 (+0200)
#           By: Louise <louise>
#
"""
The main file of this package. It contains only the
app factory (but isn't it a big part of it after all).
"""
from flask import Flask
from grandma.webapp import WEBAPP_BLUEPRINT
from grandma.api import API_BLUEPRINT

def create_app():
    """
    The app factory. Flask uses it to create the app.
    We load the config and register the blueprints.
    """
    app = Flask(__name__)

    # Load config
    app.config.from_object('grandma.config.Config')

    # Register
    app.register_blueprint(WEBAPP_BLUEPRINT)
    app.register_blueprint(API_BLUEPRINT)

    return app
