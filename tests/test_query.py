# test_query.py --- 
# 
# Filename: test_query.py
# Author: Louise <louise>
# Created: Tue Apr 21 18:57:33 2020 (+0200)
# Last-Updated: Thu Apr 23 21:02:30 2020 (+0200)
#           By: Louise <louise>
#
from grandma.bot import Query, Address
from .helpers_requests import patch_requests_no_internet
from .helpers_address import patch_address_openclassrooms
from .helpers_address import patch_address_empty
from .helpers_staticmap import patch_staticmap_openclassrooms
from .helpers_staticmap import patch_staticmap_no_key
from .helpers_wiki import patch_wiki_openclassrooms
from .helpers_wiki import patch_wiki_empty

class TestQuery:
    def test_purify_query(self):
        """
        This tests the function to remove stopwords and the like.
        """
        pure = Query.purify_query("salut grandma, est-ce que tu sais "
                                  "quelle est l'adresse d'openclassrooms")
        assert pure == "openclassrooms"

    def test_empty_query(self):
        """
        Tests that all error messages are present without a query.
        """
        query = Query("")

        assert "no-address" in query.errors
        assert "no-static-map" in query.errors
        assert "no-wiki-text" in query.errors
        assert "error-message" in query.errors
        
    def test_failed_request(self, monkeypatch):
        """
        Tests that all error messages are present without internet.
        """
        patch_requests_no_internet(monkeypatch)
        
        query = Query("openclassrooms")
        assert "error-message" in query.errors
        assert "no-address" in query.errors
        assert "no-static-map" in query.errors
        assert "no-wiki-text" in query.errors

    def test_no_staticmap(self, monkeypatch):
        """
        Test the case where all is fine except the staticmap, for
        some reason.
        """
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_no_key(monkeypatch)
        patch_wiki_openclassrooms(monkeypatch)

        query = Query("openclassrooms")
        assert "no-address" not in query.errors
        assert "no-wiki-text" not in query.errors

        assert "no-static-map" in query.errors
        
    def test_wiki_got_no_result(self, monkeypatch):
        """
        Test the case where Google Maps responds, but not Wikipedia.
        """
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_openclassrooms(monkeypatch)
        patch_wiki_empty(monkeypatch)

        query = Query("openclassrooms")
        assert "no-address" not in query.errors
        assert "no-static-map" not in query.errors
        
        assert "no-wiki-text" in query.errors
