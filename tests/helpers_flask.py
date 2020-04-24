# helpers_flask.py --- 
# 
# Filename: helpers_flask.py
# Author: Louise <louise>
# Created: Fri Apr 24 13:11:58 2020 (+0200)
# Last-Updated: Fri Apr 24 13:25:03 2020 (+0200)
#           By: Louise <louise>
# 
from grandma import create_app

def flask_get_app():
    app = create_app()
    app.config['TESTING'] = True

    return app
