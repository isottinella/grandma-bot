# test_wikitext.py --- 
# 
# Filename: test_wikitext.py
# Author: Louise <louise>
# Created: Thu Apr 23 19:32:45 2020 (+0200)
# Last-Updated: Sat Apr 25 23:13:03 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import WikiText
from .helpers_requests import patch_requests_no_internet
from .helpers_requests import patch_requests_assert_false
from .helpers_address import get_address
from .helpers_address import get_address_without_route
from .helpers_wiki import patch_wiki_openclassrooms
from .helpers_wiki import patch_wiki_search_openclassrooms
from .helpers_wiki import patch_wiki_page_missing

class Test_WikiText:
    def test_text(self, monkeypatch):
        """
        Tests that in the best case, there is a text in the object.
        """
        patch_wiki_openclassrooms(monkeypatch)

        address = get_address(monkeypatch)
        wikitext = WikiText(address)
        assert wikitext.text == "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris."

    def test_no_route(self, monkeypatch):
        """
        This test tests that the fallback mechanism works.
        """
        @staticmethod
        def get_pageid(query):
            """
            We patch this function to assert that the query is
            the one we expect, then raise IndexError to act like
            we didn't get any results, because we don't care about
            the rest.
            """
            assert query == "7 Cité Paradis, 75010 Paris, France"
            raise IndexError

        patch_requests_assert_false(monkeypatch)
        monkeypatch.setattr(WikiText, "get_pageid", get_pageid)
        
        address = get_address_without_route(monkeypatch)
        wikitext = WikiText(address)
        # Since we supposedly didn't get any results, status should
        # be False.
        assert wikitext.status == False 
        
    def test_no_extract_when_no_result(self, monkeypatch):
        """
        This test tests that the code doesn't fetch an extract when
        there's been no search result.
        """
        def requests_get(url, params = {}):
            # if there is no srsearch in params, than the request
            # is a request for an extract, and so there's been
            # a second request, and there shouldn't have been.
            assert "srsearch" in params
            
            class Dummy:
                def __init__(self):
                    pass
                def json(self):
                    with open("tests/samples/wiki_empty_response.json") as file:
                        return json.load(file)
            return Dummy()
        monkeypatch.setattr(requests, "get", requests_get)
        
        address = get_address(monkeypatch)
        wikitext = WikiText(address)

    def test_missing_page(self, monkeypatch):
        """
        This test tests the case when the API returns a result
        but the page is missing.
        """
        patch_wiki_search_openclassrooms(monkeypatch)
        patch_wiki_page_missing(monkeypatch)
        
        address = get_address(monkeypatch)
        wikitext = WikiText(address)

        assert wikitext.status == False
        
    def test_no_internet(self, monkeypatch):
        """
        This test tests that there is no result without internet.
        """
        patch_requests_no_internet(monkeypatch)
        address = get_address(monkeypatch)
        wikitext = WikiText(address)

        assert wikitext.status == False
