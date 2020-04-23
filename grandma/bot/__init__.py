# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sun Apr 19 02:22:08 2020 (+0200)
# Last-Updated: Thu Apr 23 18:52:40 2020 (+0200)
#           By: Louise <louise>
#
"""
The core of the program. Searches using the APIs and returns messages.
"""
import json
import string
import base64
import random
from pathlib import Path
import requests
from grandma.config import Config

class Query():
    """
    The core of the core. Coordinates everything else.
    Purifies a query and does all that is necessary (searching address,
    staticmap and text from Wikipedia).
    """
    # We load all stopwords (Originally the provided list, with some added, for
    # question markers, coordinate-related words and words with phatic uses).
    with (Path(__loader__.path).parent / "stopwords_fr.json").open() as file:
        STOPWORDS = json.load(file)

    # We load messages available
    with (Path(__loader__.path).parent / "messages_fr.json").open() as file:
        MESSAGES_FR = json.load(file)

    # We use the list of punctuation from the string module, without the dash
    PUNCTUATION = string.punctuation.replace("-", "")

    def __init__(self, query):
        self.errors = []
        self.error_message = ""

        self.query = self.purify_query(query)
        if not self.query:
            # If this path is taken, there was no content in the query
            # except for punctuation and stopwords. This is a fatal error.
            self.fatal_error_occured()
            self.set_error_message("Désolée, mais il ne me semble pas que tu "
                                   "m'ais demandé un lieu précis…")
            return

        self.address = Address(self.query)
        if not self.address.status:
            # If this path is taken, there was no address found for
            # the query. This is a fatal error.
            self.fatal_error_occured()
            self.set_error_message("Désolée ! Il me semble que je ne connais "
                                   "pas ce dont tu parles…")
            return

        self.staticmap = self.address.get_staticmap()
        if self.staticmap is None:
            # If this path is taken, we couldn't get a staticmap for
            # this address. This is not a fatal error.
            self.error_occured("no-static-map")

        self.wikitext = WikiText(self.address.route)
        if not self.wikitext.status:
            # If this path is taken, we couldn't get either a page
            # or the text in this page from Wikipedia for the query.
            # This is not a fatal error.
            self.error_occured("no-wiki-text")

        # Assign a message to these informations
        self.messages = self.get_messages()

    def set_error_message(self, message):
        """
        If there's an error message to get through,
        that goes through here.
        """
        self.errors.append("error-message")
        self.error_message = message

    def fatal_error_occured(self):
        """
        A fatal error occured. We add all error messages
        to the list.
        """
        self.error_occured("no-address")
        self.error_occured("no-static-map")
        self.error_occured("no-wiki-text")
        
    def error_occured(self, error):
        """
        Add an element to the list of errors.
        """
        self.errors.append(error)
        
    def get_messages(self):
        """
        Assign a random message to the address and to the funfact.
        Can be used to reassign them.
        """
        return {
            "address": random.choice(Query.MESSAGES_FR["ADDRESS"]).format(
                address=self.address.formatted_address
            ),
            # Only add this one if there is something to tell
            "funfact": random.choice(Query.MESSAGES_FR["FUNFACT"]).format(
                fact=self.wikitext.text
            ) if "no-wiki-text" not in self.errors else None
        }

    @staticmethod
    def purify_query(query):
        """
        Purify the query. By that I mean removing all unneeded characters,
        standardizing case (lowering), and removing all stopwords.
        """
        def space_if_punct(char):
            """Returns char if char isn't punctuation, a space otherwise"""
            return " " if char in Query.PUNCTUATION else char

        def is_not_stopword(word):
            """
            Pretty explicit. Is word a stopword? If yes, False. True otherwise.
            """
            return word not in Query.STOPWORDS

        # We lower the case
        lowered = query.lower()

        # We recreate a string without punctuation
        without_punct = "".join(list(map(space_if_punct, lowered)))

        # We split by spaces
        split = without_punct.split()

        # We remove all stopwords
        final = " ".join(filter(is_not_stopword, split))

        # We return the final product
        return final

class Address():
    """
    Represents an address, created from a query.
    If status is set to False, then there's been
    an error and all data associated is meaningless.
    """
    def __init__(self, query):
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

    def get_staticmap(self):
        """Returns the base64 of a map centered on this address."""
        parameters = {
            "size": Config.GMAPS_API["MAP_SIZE"],
            "zoom": Config.GMAPS_API["MAP_ZOOM"],
            "key":  Config.GMAPS_API["KEY"],
            "center": "{},{}".format(self.location["lat"],
                                     self.location["lng"]),

            "markers": "{},{}".format(self.location["lat"],
                                      self.location["lng"])
        }

        try:
            res = requests.get(Config.GMAPS_API["STATIC_ENDPOINT"],
                               params=parameters,
                               stream=True)

            if res.headers["content-type"] == "image/png":
                return "data:image/png;base64, {}".format(
                    base64.b64encode(res.content).decode()
                )
        except requests.exceptions.ConnectionError:
            return None
        return None

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
                           params=parameters)
        return res.json()["results"][0]

    @staticmethod
    def get_route(json_result):
        """Get the route component from the address"""
        for component in json_result["address_components"]:
            if "route" in component["types"]:
                return component["long_name"]
        return None

class WikiText:
    """
    This class is there to get everything there is to get from
    Wikipedia. As for Address, if status is set to False all
    data is meaningless.
    """
    def __init__(self, query):
        try:
            if not query:
                raise ValueError # There should be a query

            self.pageid = self.get_pageid(query)
            self.text = self.get_pagetext(self.pageid)
            self.status = True
        except ValueError: # There was no query
            self.status = False
        except IndexError: # No results
            self.status = False
        except KeyError: # JSON malformation
            self.status = False
        except requests.exceptions.ConnectionError: # Couldn't connect
            self.status = False

    @staticmethod
    def get_pageid(query):
        """
        Searches a page on Wikipedia corresponding to the query.
        Can raise IndexError and ConnectionError, maybe KeyError.
        """
        parameters = {
            "action": "query",
            "list": "search",
            "format": "json",
            "utf8": True,
            "srsearch": query,
            "srlimit": 1
        }

        res = requests.get(Config.WIKI_API["ENDPOINT"],
                           params=parameters)
        return res.json()["query"]["search"][0]["pageid"]

    @staticmethod
    def get_pagetext(pageid):
        """
        Gets the intro of a Page on Wikipedia, given a pageid.
        Can raise ConnectionError, but if pageid was obtained
        from get_pageid there should be no other error.
        """
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

        res = requests.get(Config.WIKI_API["ENDPOINT"],
                           params=parameters)
        return res.json()["query"]["pages"][str(pageid)]["extract"]
