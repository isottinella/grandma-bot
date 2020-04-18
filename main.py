# main.py --- 
# 
# Filename: main.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:47:03 2020 (+0200)
# Last-Updated: Sat Apr 18 20:44:45 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Flask
from webapp import webapp_blueprint
from api import api_blueprint

def main():
    app = Flask(__name__)
    app.register_blueprint(webapp_blueprint)
    app.register_blueprint(api_blueprint)
    app.run()
    
if __name__ == "__main__":
    main()
