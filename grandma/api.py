# blueprint.py --- 
# 
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 20:42:17 2020 (+0200)
# Last-Updated: Sun Apr 19 19:42:07 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api',
                          __name__,
                          url_prefix='/api')

@api_blueprint.route('/query')
def query():
    return jsonify({
        "message": request.args.get("query")
    })
