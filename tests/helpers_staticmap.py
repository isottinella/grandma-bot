# helpers_staticmap.py ---
#
# Filename: helpers_staticmap.py
# Author: Louise <louise>
# Created: Thu Apr 23 20:49:21 2020 (+0200)
# Last-Updated: Thu Apr 23 20:54:50 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import Address

def patch_staticmap_no_key(monkeypatch):
    """
    This helper patches requests.get to get the GMaps StaticMap
    API to behave as if there were no keys given.
    """
    def requests_get(url, params = {}, **kw):
        # This should only be a StaticMAP requests
        assert "staticmap" in url

        class Dummy:
            content = b"Error message"
            headers = {"content-type": "text/plain; charset=UTF-8"}
        return Dummy()
    monkeypatch.setattr(requests, "get", requests_get)

def patch_staticmap_png(monkeypatch):
    """
    This helper patches requests.get to get the GMaps StaticMap
    API to return a dummy PNG.
    """
    def requests_get(url, params = {}, **kw):
        # This should only be a StaticMAP requests
        assert "staticmap" in url

        class Dummy:
            with open("tests/samples/staticmap_png.png", "rb") as file:
                content = file.read()
            headers = {"content-type": "image/png"}
        return Dummy()
    monkeypatch.setattr(requests, "get", requests_get)

def patch_staticmap_openclassrooms(monkeypatch):
    """
    This helper patches get_staticmap to return the one for
    openclassrooms.
    """
    def get_staticmap(address):
        with open("tests/samples/staticmap_openclassrooms.json") as file:
            return json.load(file)
    monkeypatch.setattr(Address, "get_staticmap", get_staticmap)
