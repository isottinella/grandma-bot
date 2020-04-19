# bot.py --- 
# 
# Filename: bot.py
# Author: Louise <louise>
# Created: Sun Apr 19 02:22:35 2020 (+0200)
# Last-Updated: Sun Apr 19 19:16:59 2020 (+0200)
#           By: Louise <louise>
#
import requests
from grandma.config import Config

class Query():
    def __init__(self, query):
        self.query = query
        self.address = Query.get_address(query)

    @staticmethod
    def get_address(query):
        json = Query.get_address_json(query)
        return Address(json)
        
    @staticmethod
    def get_address_json(query):
        parameters = {
            "address": query,
            "region": Config.GMAPS_API["REGION"],
            "key": Config.GMAPS_API["KEY"]
        }

        res = requests.get(Config.GMAPS_API["PLACES_ENDPOINT"],
                           params = parameters)
        return res.json()["results"][0]

class Address():
    def __init__(self, json):
        self.formatted_address = json["formatted_address"]
        self.location = json["geometry"]["location"]

        # Find the street name
        for component in json["address_components"]:
            if "route" in component["types"]:
                self.route = component["long_name"]
                break
