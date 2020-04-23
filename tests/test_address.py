# test_address.py --- 
# 
# Filename: test_address.py
# Author: Louise <louise>
# Created: Sun Apr 19 18:29:08 2020 (+0200)
# Last-Updated: Thu Apr 23 21:05:08 2020 (+0200)
#           By: Louise <louise>
#
from grandma.bot import Address
from .helpers_requests import patch_requests_no_internet
from .helpers_address import patch_address_openclassrooms
from .helpers_address import patch_address_without_route
from .helpers_address import patch_address_empty
from .helpers_staticmap import patch_staticmap_png
from .helpers_staticmap import patch_staticmap_no_key

class TestAddress:
    def test_address_formatted(self, monkeypatch):
        """
        Tests if address_formated is correct and exists.
        """
        patch_address_openclassrooms(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.formatted_address == "7 Cité Paradis, 75010 Paris, France"

    def test_address_route(self, monkeypatch):
        """
        Tests if route is correct and exists
        """
        patch_address_openclassrooms(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.route == "Cité Paradis"

    def test_address_location(self, monkeypatch):
        """
        Tests if location is correct and exists
        """
        patch_address_openclassrooms(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.location["lat"] == 48.8748465
        assert address.location["lng"] == 2.3504873

    def test_address_no_route(self, monkeypatch):
        """
        Tests whether the code still works when there is no route
        in the address.
        """
        patch_address_without_route(monkeypatch)

        address = Address("openclassrooms")
        assert address.status
        assert address.route is None
        
    def test_address_no_response(self, monkeypatch):
        """
        Tests that the status is False when GMaps doesn't give
        a result.
        """
        patch_address_empty(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.status == False

    def test_staticmap_correct(self, monkeypatch):
        """
        Tests that the get_staticmap method works in the
        best case.
        """
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_png(monkeypatch)

        address = Address("openclassrooms")
        staticmap = address.get_staticmap()
        assert staticmap == ("data:image/png;base64, iVBORw0KGgoAAAANSUhEUg"
                             "AAAAEAAAABAQMAAAAl21bKAAAAA1BMVEX/TQBcNTh/AAA"
                             "AAXRSTlPM0jRW/QAAAApJREFUeJxjYgAAAAYAAzY3fKgA"
                             "AAAASUVORK5CYII=")

    def test_staticmap_no_key(self, monkeypatch):
        """
        Tests that the get_staticmap method returns
        None without a key
        """
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_no_key(monkeypatch)

        address = Address("openclassrooms")
        staticmap = address.get_staticmap()
        assert staticmap is None

    def test_staticmap_no_internet(self, monkeypatch):
        """
        Tests that the get_staticmap method returns
        None without Internet (this shouldn't be a 
        problem given the fact that we usually don't
        get this far without Internet).
        """
        patch_address_openclassrooms(monkeypatch)
        patch_requests_no_internet(monkeypatch)

        address = Address("openclassrooms")
        staticmap = address.get_staticmap()
        assert staticmap is None
