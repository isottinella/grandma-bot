# blueprint.py --- 
# 
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 20:42:17 2020 (+0200)
# Last-Updated: Sat Apr 18 20:45:15 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint

api_blueprint = Blueprint('api',
                          __name__,
                          url_prefix='/api')
