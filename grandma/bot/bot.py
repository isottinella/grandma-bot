# bot.py --- 
# 
# Filename: bot.py
# Author: Louise <louise>
# Created: Sun Apr 19 02:22:35 2020 (+0200)
# Last-Updated: Wed Apr 22 21:09:25 2020 (+0200)
#           By: Louise <louise>
#
import requests, json, string
from pathlib import Path
from flask import current_app
from grandma.config import Config

class Query():
    # We load all stopwords as class constants
    with open(Path(__loader__.path).parent / "stopwords_fr.json") as file:
        STOPWORDS_FR = json.load(file)
    STOPWORDS_QUESTION = ["connais", "cherche", "sais", "penses", "quoi",
                          "dis", "entendu", "parlé", "est-ce", "connaitrais"]
    STOPWORDS_COORD = ["adresse", "emplacement", "endroit", "lieu", "lieu",
                       "place", "coordonnées"]
    STOPWORDS_PHATIQUE = ["salut", "bonjour", "coucou", "ciao", "yo", "salve",
                          "ave", "salutations", "wesh", "grandpy", "grandma",
                          "mamie", "mamy", "mémé", "papi", "papy",
                          "pépé", "grand-mère", "grand-père"]
    STOPWORDS = (STOPWORDS_FR + STOPWORDS_QUESTION + STOPWORDS_COORD
                 + STOPWORDS_PHATIQUE)

    # We use the list of punctuation from the string module, without the dash
    PUNCTUATION = string.punctuation.replace("-", "")
    
    def __init__(self, query):
        self.query = self.purify_query(query)
        if not self.query:
            self.state = "no-address"
            self.message = ("Désolée, mais il ne me semble pas que tu m'ais "
                            "demandé un lieu précis…")
            return # Having no query except for stopwords is a fatal error
        
        self.address = self.get_address(self.query)
        if self.address is None:
            self.state = "no-address"
            self.message = ("Désolée ! Il me semble que je ne connais pas ce "
                            "dont tu parles…")
            return # Having no address is a fatal error.
        
        self.static_map = self.get_staticmap(self.address)
        
        self.message = self.address.formatted_address

    @staticmethod
    def purify_query(query):
        # We lower the case
        lowered = query.lower()
        
        # We recreate a string without punctuation
        space_if_punct = lambda c: " " if c in Query.PUNCTUATION else c
        without_punct = "".join(list(map(space_if_punct, lowered)))

        # We split by spaces
        split = without_punct.split()
        
        # We remove all stopwords
        is_not_stopword = lambda word: word not in Query.STOPWORDS
        final = " ".join(filter(is_not_stopword, split))

        # We return the final product
        return final
        
    @staticmethod
    def get_address(query):
        try:
            json = Query.get_address_json(query)
            return None if json is None else Address(json)
        except KeyError:
            return None
        
    @staticmethod
    def get_address_json(query):
        parameters = {
            "address": query,
            "region": Config.GMAPS_API["REGION"],
            "key": Config.GMAPS_API["KEY"]
        }

        res = requests.get(Config.GMAPS_API["PLACES_ENDPOINT"],
                           params = parameters)
        try:
            return res.json()["results"][0]
        except IndexError:
            return None
        except requests.exceptions.ConnectionError:
            return None

    @staticmethod
    def get_staticmap(address):
        return None

class Address():
    def __init__(self, json):
        self.formatted_address = json["formatted_address"]
        self.location = json["geometry"]["location"]
        
        # Find the street name
        for component in json["address_components"]:
            if "route" in component["types"]:
                self.route = component["long_name"]
                break
