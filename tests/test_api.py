# test_api.py --- 
# 
# Filename: test_api.py
# Author: Louise <louise>
# Created: Fri Apr 24 13:10:18 2020 (+0200)
# Last-Updated: Fri Apr 24 13:34:44 2020 (+0200)
#           By: Louise <louise>
#
import json
from .helpers_flask import flask_get_app
from .helpers_address import patch_address_openclassrooms
from .helpers_address import patch_address_empty
from .helpers_staticmap import patch_staticmap_openclassrooms
from .helpers_wiki import patch_wiki_openclassrooms

class TestApi:
    def test_normal_request(self, monkeypatch):
        """
        This tests the best case.
        """
        app = flask_get_app()
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_openclassrooms(monkeypatch)
        patch_wiki_openclassrooms(monkeypatch)

        with app.test_client() as client:
            rv = client.get("/api/query?query='openclassrooms'")

            assert rv._status_code == 200
            assert rv.headers["Content-Type"] == "application/json"

            content = json.loads(rv.get_data())
            # Check the JSON is well-formed
            assert "error_message" in content
            assert not content["error_message"]
            assert "errors" in content
            assert not content["errors"]
            assert "messages" in content
            assert len(content["messages"]) == 2
            assert "staticmap" in content
            assert content["staticmap"]

    def test_no_address(self, monkeypatch):
        """
        This tests the fatal error case.
        """
        app = flask_get_app()
        patch_address_empty(monkeypatch)
        patch_staticmap_openclassrooms(monkeypatch)
        patch_wiki_openclassrooms(monkeypatch)
        
        with app.test_client() as client:
            rv = client.get("/api/query?query='openclassrooms'")
            
            assert rv._status_code == 200
            assert rv.headers["Content-Type"] == "application/json"
            
            content = json.loads(rv.get_data())
            # Check the JSON is well-formed and has the errors
            assert "error_message" in content
            assert content["error_message"]
            assert "errors" in content
            assert len(content["errors"]) == 4
            assert "messages" in content
            assert content["messages"] is None
            assert "staticmap" in content
            assert content["staticmap"] is None
