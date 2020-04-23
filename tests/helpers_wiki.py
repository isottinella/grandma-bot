# helpers_wiki.py ---
#
# Filename: helpers_wiki.py
# Author: Louise <louise>
# Created: Thu Apr 23 20:50:05 2020 (+0200)
# Last-Updated: Thu Apr 23 20:50:28 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import WikiText

def patch_wiki_search_openclassrooms(monkeypatch):
    """
    This helper patches get_pageid  to get a good
    result from Wikipedia for the query 'cité paradis'
    """
    @staticmethod
    def get_pageid(query):
        return 5653202
    monkeypatch.setattr(WikiText, "get_pageid", get_pageid)

def patch_wiki_page_missing(monkeypatch):
    """
    This helper patches requests.get to get the Wikipedia API
    to return a missing page.
    """
    def requests_get(url, params = {}, **kw):
        class Dummy:
            def json(self):
                with open("tests/samples/wiki_extract_missing.json") as file:
                    return json.load(file)
        return Dummy()
    monkeypatch.setattr(requests, "get", requests_get)

def patch_wiki_page_openclassrooms(monkeypatch):
    """
    This helper patches get_pagetext to get a good result
    for the 'cité paradis' page.
    """
    @staticmethod
    def get_pagetext(pageid):
        return "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris."
    monkeypatch.setattr(WikiText, "get_pagetext", get_pagetext)

def patch_wiki_openclassrooms(monkeypatch):
    """
    This helper combines the two aforementioned helpers.
    """
    patch_wiki_search_openclassrooms(monkeypatch)
    patch_wiki_page_openclassrooms(monkeypatch)

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
