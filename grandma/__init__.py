# main.py --- 
# 
# Filename: main.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:47:03 2020 (+0200)
# Last-Updated: Sun Apr 19 02:46:19 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Flask
from grandma.webapp import webapp_blueprint
from grandma.api import api_blueprint

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object('grandma.config.Config')

    # Register
    app.register_blueprint(webapp_blueprint)
    app.register_blueprint(api_blueprint)
    
    return app

