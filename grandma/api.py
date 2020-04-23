# blueprint.py --- 
# 
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 20:42:17 2020 (+0200)
# Last-Updated: Thu Apr 23 17:20:26 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint, jsonify, request
from grandma.bot import Query

api_blueprint = Blueprint('api',
                          __name__,
                          url_prefix='/api')

@api_blueprint.route('/query')
def query():
    query = Query(request.args.get("query"))
    
    return jsonify({
        "address": query.message_address,
        "staticmap": query.staticmap,
        "funfact": query.message_funfact,
        "errors": query.errors,
    })
