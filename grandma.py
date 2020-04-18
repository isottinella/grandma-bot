# main.py --- 
# 
# Filename: main.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:47:03 2020 (+0200)
# Last-Updated: Sat Apr 18 20:55:49 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Flask
from webapp import webapp_blueprint
from api import api_blueprint

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(webapp_blueprint)
    app.register_blueprint(api_blueprint)

    return app

