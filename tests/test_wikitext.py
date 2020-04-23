# test_wikitext.py --- 
# 
# Filename: test_wikitext.py
# Author: Louise <louise>
# Created: Thu Apr 23 19:32:45 2020 (+0200)
# Last-Updated: Thu Apr 23 19:54:04 2020 (+0200)
#           By: Louise <louise>
#
import json
import requests
from grandma.bot import WikiText
from .helpers import patch_requests_no_internet
from .helpers import patch_wiki_openclassrooms

class Test_WikiText:
    def test_text(self, monkeypatch):
        patch_wiki_openclassrooms(monkeypatch)

        wikitext = WikiText("cité paradis")
        assert wikitext.text == "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris."

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
