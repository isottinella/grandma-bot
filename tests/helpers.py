# helpers.py --- 
# 
# Filename: helpers.py
# Author: Louise <louise>
# Created: Thu Apr 23 19:12:16 2020 (+0200)
# Last-Updated: Thu Apr 23 19:30:49 2020 (+0200)
#           By: Louise <louise>
# 
import json
import requests
from grandma.bot import Query, Address

def get_openclassrooms_address(monkeypatch):
    def get_address_json(query):
        with open("tests/samples/openclassrooms_places.json") as file:
            return json.load(file)
        
    monkeypatch.setattr(Address, "get_address_json", get_address_json)
    return Address("openclassrooms")

def get_empty_address(monkeypatch):
    def get_address_json(query):
        with open("tests/samples/gmaps_empty_response.json") as file:
            return json.load(file)
        
    monkeypatch.setattr(Address, "get_address_json", get_address_json)
    return Address("openclassrooms")

def get_query_without_internet(monkeypatch):
    def failed_request(url, params = []):
        raise requests.exceptions.ConnectionError
        
    monkeypatch.setattr(requests, "get", failed_request)
    return Query("openclassrooms")
