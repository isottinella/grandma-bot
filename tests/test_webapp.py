# test_webapp.py --- 
# 
# Filename: test_webapp.py
# Author: Louise <louise>
# Created: Fri Apr 24 13:35:21 2020 (+0200)
# Last-Updated: Fri Apr 24 13:37:53 2020 (+0200)
#           By: Louise <louise>
# 
from .helpers_flask import flask_get_app

class TestWebApp():
    def test_webapp(self):
        """
        There is only one way this can go.
        """
        app = flask_get_app()

        with app.test_client() as client:
            rv = client.get("/")

            assert rv._status_code == 200
            assert rv.headers["Content-Type"] == "text/html; charset=utf-8"
            # Check the url_for completed
            assert b"/api/query" in rv.get_data()
