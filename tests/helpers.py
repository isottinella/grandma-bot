# helpers.py --- 
# 
# Filename: helpers.py
# Author: Louise <louise>
# Created: Thu Apr 23 19:12:16 2020 (+0200)
# Last-Updated: Thu Apr 23 19:50:53 2020 (+0200)
#           By: Louise <louise>
# 
import json
import requests
from grandma.bot import Query, Address, WikiText

def patch_address_openclassrooms(monkeypatch):
    def get_address_json(query):
        with open("tests/samples/openclassrooms_places.json") as file:
            return json.load(file)
        
    monkeypatch.setattr(Address, "get_address_json", get_address_json)

def patch_address_empty(monkeypatch):
    def get_address_json(query):
        with open("tests/samples/gmaps_empty_response.json") as file:
            return json.load(file)
        
    monkeypatch.setattr(Address, "get_address_json", get_address_json)

def patch_staticmap_openclassrooms(monkeypatch):
    def get_staticmap(address):
        with open("tests/samples/openclassrooms_staticmap.json") as file:
            return json.load(file)
    monkeypatch.setattr(Address, "get_staticmap", get_staticmap)

def patch_wiki_openclassrooms(monkeypatch):
    @staticmethod
    def get_pageid(query):
        return 5653202
    monkeypatch.setattr(WikiText, "get_pageid", get_pageid)

    @staticmethod
    def get_pagetext(pageid):
        return "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris."
    monkeypatch.setattr(WikiText, "get_pagetext", get_pagetext)
    
def patch_wiki_empty(monkeypatch):
    def requests_get(url, params = {}):
        class Dummy:
            def __init__(self):
                pass
            def json(self):
                with open("tests/samples/wiki_empty_response.json") as file:
                    return json.load(file)
        return Dummy()
    monkeypatch.setattr(requests, "get", requests_get)
    
def patch_requests_no_internet(monkeypatch):
    def failed_request(url, params = []):
        raise requests.exceptions.ConnectionError
        
    monkeypatch.setattr(requests, "get", failed_request)
