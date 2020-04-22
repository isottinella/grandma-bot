# bot.py --- 
# 
# Filename: bot.py
# Author: Louise <louise>
# Created: Sun Apr 19 02:22:35 2020 (+0200)
# Last-Updated: Thu Apr 23 01:27:21 2020 (+0200)
#           By: Louise <louise>
#
import requests, json, string, base64
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
        self.errors = []
        
        self.query = self.purify_query(query)
        if not self.query:
            self.errors.append("no-address")
            self.message = ("Désolée, mais il ne me semble pas que tu m'ais "
                            "demandé un lieu précis…")
            return # Having no query except for stopwords is a fatal error
        
        self.address = self.get_address(self.query)
        if self.address is None:
            self.errors.append("no-address")
            self.message = ("Désolée ! Il me semble que je ne connais pas ce "
                            "dont tu parles…")
            return # Having no address is a fatal error.
        
        self.staticmap = self.get_staticmap(self.address)
        if self.staticmap is None: # This is not a fatal error
            self.errors.append("no-static-map")

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

        try:
            res = requests.get(Config.GMAPS_API["PLACES_ENDPOINT"],
                               params = parameters)
            return res.json()["results"][0]
        except IndexError:
            return None
        except requests.exceptions.ConnectionError:
            return None

    @staticmethod
    def get_staticmap(address):
        parameters = {
            "size": Config.GMAPS_API["MAP_SIZE"],
            "zoom": Config.GMAPS_API["MAP_ZOOM"],
            "key":  Config.GMAPS_API["KEY"],
            "center": "{},{}".format(address.location["lat"],
                                     address.location["lng"]),
            
            "markers": "{},{}".format(address.location["lat"],
                                     address.location["lng"])
        }

        try:
            res = requests.get(Config.GMAPS_API["STATIC_ENDPOINT"],
                               params = parameters,
                               stream = True)
            
            if res.headers["content-type"] == "image/png":
                return "data:image/png;base64, {}".format(
                    base64.b64encode(res.content).decode()
                )
            else:
                return None
        except requests.exceptions.ConnectionError:
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
