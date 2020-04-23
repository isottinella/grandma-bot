# helpers.py --- 
# 
# Filename: helpers.py
# Author: Louise <louise>
# Created: Thu Apr 23 19:12:16 2020 (+0200)
# Last-Updated: Thu Apr 23 20:30:39 2020 (+0200)
#           By: Louise <louise>
# 
import json
import requests
from grandma.bot import Query, Address, WikiText

def patch_address_openclassrooms(monkeypatch):
    """
    This helper patches get_address_json to always return
    the result for the query 'openclassrooms'.
    """
    def get_address_json(query):
        with open("tests/samples/openclassrooms_places.json") as file:
            return json.load(file)
        
    monkeypatch.setattr(Address, "get_address_json", get_address_json)

def patch_address_empty(monkeypatch):
    """
    This helper patches requests.get to always behave as if
    GMaps said there were no results.
    """
    def requests_get(url, params = {}, **kw):
        # This should only be a request for an address
        assert "address" in params

        class Dummy:
            def json(self):
                with open("tests/samples/gmaps_empty_response.json") as file:
                    return json.load(file)
        return Dummy()
    monkeypatch.setattr(requests, "get", requests_get)

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
            with open("tests/samples/empty_png.png", "rb") as file:
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
        with open("tests/samples/openclassrooms_staticmap.json") as file:
            return json.load(file)
    monkeypatch.setattr(Address, "get_staticmap", get_staticmap)

def patch_wiki_openclassrooms(monkeypatch):
    """
    This helper patches get_pageid and get_pagetext to get a good
    result from Wikipedia for the query 'cité paradis'
    """
    @staticmethod
    def get_pageid(query):
        return 5653202
    monkeypatch.setattr(WikiText, "get_pageid", get_pageid)

    @staticmethod
    def get_pagetext(pageid):
        return "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris."
    monkeypatch.setattr(WikiText, "get_pagetext", get_pagetext)
    
def patch_wiki_empty(monkeypatch):
    """
    This helper patches requests.get to get the Wikipedia API
    to return an empty search list.
    """
    def requests_get(url, params = {}, **kw):
        class Dummy:
            def json(self):
                with open("tests/samples/wiki_empty_response.json") as file:
                    return json.load(file)
        return Dummy()
    monkeypatch.setattr(requests, "get", requests_get)
    
def patch_requests_no_internet(monkeypatch):
    """
    This helper patches requests.get to behave as if
    there is no internet connection.
    """
    def failed_request(url, params = {}, **kw):
        raise requests.exceptions.ConnectionError
        
    monkeypatch.setattr(requests, "get", failed_request)

def patch_requests_assert_false(monkeypatch):
    """
    This function is useful to guarantee no requests is made.
    """
    def requests_get(url, params = {}, **kw):
        assert False

    monkeypatch.setattr(requests, "get", requests_get)
