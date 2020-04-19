# config.py.tmpl --- 
# 
# Filename: config.py.tmpl
# Author: Louise <louise>
# Created: Sat Apr 18 20:49:13 2020 (+0200)
# Last-Updated: Sun Apr 19 02:49:53 2020 (+0200)
#           By: Louise <louise>
# 
import os

class Config:
    # Put here your Google Maps API key
    GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")
    
    # Set this to production when you go into production
    ENV = "development"
    
    # Set this to false when you go into production
    DEBUG = True

    # Set this to true when you test
    TESTING = True
