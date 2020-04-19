# config.py.tmpl --- 
# 
# Filename: config.py.tmpl
# Author: Louise <louise>
# Created: Sat Apr 18 20:49:13 2020 (+0200)
# Last-Updated: Sun Apr 19 19:42:13 2020 (+0200)
#           By: Louise <louise>
# 
import os, json

class Config:
    GMAPS_API = {
        'PLACES_ENDPOINT': "https://maps.googleapis.com/maps/api/geocode/json",
        'STATIC_ENDPOINT': "",
        'KEY': os.environ.get("GMAPS_API_KEY"),
        'REGION': "FR"
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
