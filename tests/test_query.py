# test_query.py --- 
# 
# Filename: test_query.py
# Author: Louise <louise>
# Created: Tue Apr 21 18:57:33 2020 (+0200)
# Last-Updated: Thu Apr 23 19:28:23 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import Query, Address
from .helpers import get_query_without_internet

class TestQuery:
    def test_purify_query(self):
        pure = Query.purify_query("salut grandma, est-ce que tu sais "
                           "quelle est l'adresse d'openclassrooms")
        assert pure == "openclassrooms"

    def test_failed_request(self, monkeypatch):
        query = get_query_without_internet(monkeypatch)
        assert "error-message" in query.errors
        assert "no-address" in query.errors
        assert "no-static-map" in query.errors
        assert "no-wiki-text" in query.errors

    def test_wiki_got_no_result(self, monkeypatch):
        """
        Test the case where Google Maps responds, but not Wikipedia.
        """
        # patch get_address_json
        def get_address_json(query):
            with open("tests/samples/openclassrooms_places.json") as file:
                return json.load(file)
        monkeypatch.setattr(Address, "get_address_json", get_address_json)
            
        # patch get_staticmap
        def get_staticmap(address):
            with open("tests/samples/openclassrooms_staticmap.json") as file:
                return json.load(file)
        monkeypatch.setattr(Address, "get_staticmap", get_staticmap)

        # patch requests.get to get a fake response from Wikipedia
        def requests_get(url, params = {}):
            # We assert that the request is a search
            assert "srsearch" in params
            
            class Dummy:
                def __init__(self):
                    pass
                def json(self):
                    with open("tests/samples/wiki_empty_response.json") as file:
                        return json.load(file)
            return Dummy()
        monkeypatch.setattr(requests, "get", requests_get)

        query = Query("openclassrooms")
        assert "no-address" not in query.errors
        assert "no-static-map" not in query.errors
        
        assert "no-wiki-text" in query.errors
