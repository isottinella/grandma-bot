# test_address.py --- 
# 
# Filename: test_address.py
# Author: Louise <louise>
# Created: Sun Apr 19 18:29:08 2020 (+0200)
# Last-Updated: Sun Apr 19 19:20:41 2020 (+0200)
#           By: Louise <louise>
#
import json
from grandma.bot import Query

def get_query_address(monkeypatch):
    def get_address_json(query):
        with open("tests/samples/openclassrooms_places.json") as file:
            return json.load(file)
        
    monkeypatch.setattr(Query, "get_address_json", get_address_json)
    query = Query("openclassrooms")
    return query.address

class TestAddress:
    def test_address_formatted(self, monkeypatch):
        address = get_query_address(monkeypatch)
        assert address.formatted_address == "7 Cité Paradis, 75010 Paris, France"

    def test_address_route(self, monkeypatch):
        address = get_query_address(monkeypatch)
        assert address.route == "Cité Paradis"

    def test_address_location(self, monkeypatch):
        address = get_query_address(monkeypatch)
        assert address.location["lat"] == 48.8748465
        assert address.location["lng"] == 2.3504873
