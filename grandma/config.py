# config.py ---
#
# Filename: config.py
# Author: Louise <louise>
# Created: Sat Apr 18 20:49:13 2020 (+0200)
# Last-Updated: Thu Apr 23 17:53:28 2020 (+0200)
#           By: Louise <louise>
#
"""
Contains the Config class.
"""
import os

class Config:
    """
    The config of the app, and everything that is needed to get it up
    and running. Any changes will be made here.
    """
    # Disable the too few public method warning from pylint
    # pylint: disable=too-few-public-methods
    GMAPS_API = {
        'PLACES_ENDPOINT': "https://maps.googleapis.com/maps/api/geocode/json",
        'STATIC_ENDPOINT': "https://maps.googleapis.com/maps/api/staticmap",
        'KEY': os.environ.get("GMAPS_API_KEY"),
        'REGION': "FR",
        'MAP_SIZE': "500x300",
        'MAP_ZOOM': "16"
    }

    WIKI_API = {
        'ENDPOINT': "https://fr.wikipedia.org/w/api.php",
    }

    # Set this to production when you go into production
    ENV = "development"

    # Set this to false when you go into production
    DEBUG = True

    # Set this to true when you test
    TESTING = True
