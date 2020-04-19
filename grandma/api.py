# blueprint.py --- 
# 
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 20:42:17 2020 (+0200)
# Last-Updated: Sun Apr 19 03:29:17 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api',
                          __name__,
                          url_prefix='/api')

@api_blueprint.route('/')
def index():
    return jsonify({
        "message": "API index"
    })
