# test_address.py --- 
# 
# Filename: test_address.py
# Author: Louise <louise>
# Created: Sun Apr 19 18:29:08 2020 (+0200)
# Last-Updated: Thu Apr 23 19:30:34 2020 (+0200)
#           By: Louise <louise>
#
from .helpers import get_openclassrooms_address, get_empty_address

class TestAddress:
    def test_address_formatted(self, monkeypatch):
        address = get_openclassrooms_address(monkeypatch)
        assert address.formatted_address == "7 Cité Paradis, 75010 Paris, France"

    def test_address_route(self, monkeypatch):
        address = get_openclassrooms_address(monkeypatch)
        assert address.route == "Cité Paradis"

    def test_address_location(self, monkeypatch):
        address = get_openclassrooms_address(monkeypatch)
        assert address.location["lat"] == 48.8748465
        assert address.location["lng"] == 2.3504873

    def test_address_no_response(self, monkeypatch):
        address = get_empty_address(monkeypatch)
        assert address.status == False
