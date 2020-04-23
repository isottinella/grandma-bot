# address_helpers.py ---
#
# Filename: address_helpers.py
# Author: Louise <louise>
# Created: Thu Apr 23 20:48:08 2020 (+0200)
# Last-Updated: Thu Apr 23 20:48:46 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import Address

def patch_address_openclassrooms(monkeypatch):
    """
    This helper patches get_address_json to always return
    the result for the query 'openclassrooms'.
    """
    def get_address_json(query):
        with open("tests/samples/gmaps_openclassrooms.json") as file:
            return json.load(file)

    monkeypatch.setattr(Address, "get_address_json", get_address_json)

def patch_address_without_route(monkeypatch):
    """
    This helper patches get_address_json to always return
    a result without a route in the components.
    """
    def get_address_json(query):
        with open("tests/samples/gmaps_without_route.json") as file:
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
