# bot.py --- 
# 
# Filename: bot.py
# Author: Louise <louise>
# Created: Sun Apr 19 02:22:35 2020 (+0200)
# Last-Updated: Thu Apr 23 17:32:49 2020 (+0200)
#           By: Louise <louise>
#
import json
import string
import base64
import random
from pathlib import Path
import requests
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

    # We load messages available
    with open(Path(__loader__.path).parent / "messages_fr.json") as file:
        MESSAGES_FR = json.load(file)

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
        if not self.address.status:
            self.errors.append("no-address")
            self.message = ("Désolée ! Il me semble que je ne connais pas ce "
                            "dont tu parles…")
            return # Having no address is a fatal error.
        
        self.staticmap = self.get_staticmap(self.address)
        if self.staticmap is None: # This is not a fatal error
            self.errors.append("no-static-map")

        self.wikitext = self.get_wikitext(self.address)
        if self.wikitext is None: # This is not a fatal error
            self.errors.append("no-wiki-text")

        # Assign a message to these informations
        self.message_address = random.choice(
            Query.MESSAGES_FR["ADDRESS"]
        ).format(
            address = self.address.formatted_address
        )
        if "no-wiki-text" not in self.errors:
            self.message_funfact = random.choice(
                Query.MESSAGES_FR["FUNFACT"]
            ).format(
                fact = self.wikitext
            )

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

    @staticmethod
    def get_wikitext(address):
        query = address.route
        if query:
            page = Query.get_wikipage(query)
            text = Query.get_pagetext(page)
            return text

    @staticmethod
    def get_wikipage(query):
        parameters = {
            "action": "query",
            "list": "search",
            "format": "json",
            "utf8": True,
            "srsearch": query,
            "srlimit": 1
        }

        try:
            res = requests.get(Config.WIKI_API["ENDPOINT"],
                               params = parameters)
            return res.json()["query"]["search"][0]["pageid"]
        except IndexError: # No results
            return None
        except KeyError: # JSON malformation
            return None
        except requests.exceptions.ConnectionError: # Couldn't connect
            return None

    @staticmethod
    def get_pagetext(pageid):
        parameters = {
            "action": "query",
            "utf8": True,
            "format": "json",
            "pageids": pageid,
            "prop": "extracts",
            "exlimit": 1,
            "explaintext": True,
            "exintro": True
        }

        try:
            res = requests.get(Config.WIKI_API["ENDPOINT"],
                               params = parameters)
            return res.json()["query"]["pages"][str(pageid)]["extract"]
        except IndexError: # No results
            return None
        except KeyError: # JSON malformation
            return None
        except requests.exceptions.ConnectionError: # Couldn't connect
            return None
        

class Address():
    def __init__(self, query):
        """
        Creates a new Address object. 
        Sets status to False if an error is raised.
        """
        try:
            json_result = Address.get_address_json(query)
            self.formatted_address = json_result["formatted_address"]
            self.location = json_result["geometry"]["location"]
            self.route = Address.get_route(json_result)
            self.status = True
        except KeyError: # JSON malformation
            self.status = False
        except IndexError: # No results
            self.status = False
        except requests.exceptions.ConnectionError:
            self.status = False
        
    @staticmethod
    def get_address_json(query):
        """
        Gets the result of a query to GMAPS API for a given query.
        """
        parameters = {
            "address": query,
            "region": Config.GMAPS_API["REGION"],
            "key": Config.GMAPS_API["KEY"]
        }

        res = requests.get(Config.GMAPS_API["PLACES_ENDPOINT"],
                           params = parameters)
        return res.json()["results"][0]

    @staticmethod
    def get_route(json_result):
        """Get the route component from the address"""
        for component in json_result["address_components"]:
            if "route" in component["types"]:
                return component["long_name"]
        return None
