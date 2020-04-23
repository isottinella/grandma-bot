# test_wikitext.py --- 
# 
# Filename: test_wikitext.py
# Author: Louise <louise>
# Created: Thu Apr 23 19:32:45 2020 (+0200)
# Last-Updated: Thu Apr 23 21:01:31 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import WikiText
from .helpers_requests import patch_requests_no_internet
from .helpers_requests import patch_requests_assert_false
from .helpers_wiki import patch_wiki_openclassrooms
from .helpers_wiki import patch_wiki_search_openclassrooms
from .helpers_wiki import patch_wiki_page_missing

class Test_WikiText:
    def test_text(self, monkeypatch):
        """
        Tests that in the best case, there is a text in the object.
        """
        patch_wiki_openclassrooms(monkeypatch)

        wikitext = WikiText("cité paradis")
        assert wikitext.text == "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris."

    def test_no_query(self, monkeypatch):
        """
        This test tests that without a query there is no result.
        """
        patch_requests_assert_false(monkeypatch)

        wikitext = WikiText(None)
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

        wikitext = WikiText("cité paradis")

    def test_missing_page(self, monkeypatch):
        """
        This test tests the case when the API returns a result
        but the page is missing.
        """
        patch_wiki_search_openclassrooms(monkeypatch)
        patch_wiki_page_missing(monkeypatch)
        wikitext = WikiText("cité paradis")

        assert wikitext.status == False
        
    def test_no_internet(self, monkeypatch):
        """
        This test tests that there is no result without internet.
        """
        patch_requests_no_internet(monkeypatch)
        wikitext = WikiText("cité paradis")

        assert wikitext.status == False
