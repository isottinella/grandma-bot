# test_address.py --- 
# 
# Filename: test_address.py
# Author: Louise <louise>
# Created: Sun Apr 19 18:29:08 2020 (+0200)
# Last-Updated: Thu Apr 23 20:29:57 2020 (+0200)
#           By: Louise <louise>
#
from grandma.bot import Address
from .helpers import patch_requests_no_internet
from .helpers import patch_address_openclassrooms, patch_address_empty
from .helpers import patch_staticmap_png, patch_staticmap_no_key

class TestAddress:
    def test_address_formatted(self, monkeypatch):
        """
        Test if address_formated is correct and exists.
        """
        patch_address_openclassrooms(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.formatted_address == "7 Cité Paradis, 75010 Paris, France"

    def test_address_route(self, monkeypatch):
        """
        Test if route is correct and exists
        """
        patch_address_openclassrooms(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.route == "Cité Paradis"

    def test_address_location(self, monkeypatch):
        """
        Test if location is correct and exists
        """
        patch_address_openclassrooms(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.location["lat"] == 48.8748465
        assert address.location["lng"] == 2.3504873

    def test_address_no_response(self, monkeypatch):
        patch_address_empty(monkeypatch)
        
        address = Address("openclassrooms")
        assert address.status == False

    def test_staticmap_correct(self, monkeypatch):
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_png(monkeypatch)

        address = Address("openclassrooms")
        staticmap = address.get_staticmap()
        assert staticmap == ("data:image/png;base64, iVBORw0KGgoAAAANSUhEUg"
                             "AAAAEAAAABAQMAAAAl21bKAAAAA1BMVEX/TQBcNTh/AAA"
                             "AAXRSTlPM0jRW/QAAAApJREFUeJxjYgAAAAYAAzY3fKgA"
                             "AAAASUVORK5CYII=")

    def test_staticmap_no_key(self, monkeypatch):
        patch_address_openclassrooms(monkeypatch)
        patch_staticmap_no_key(monkeypatch)

        address = Address("openclassrooms")
        staticmap = address.get_staticmap()
        assert staticmap is None

    def test_staticmap_no_internet(self, monkeypatch):
        patch_address_openclassrooms(monkeypatch)
        patch_requests_no_internet(monkeypatch)

        address = Address("openclassrooms")
        staticmap = address.get_staticmap()
        assert staticmap is None
