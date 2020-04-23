# blueprint.py ---
#
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 20:42:17 2020 (+0200)
# Last-Updated: Thu Apr 23 18:52:49 2020 (+0200)
#           By: Louise <louise>
#
"""
This module creates the API blueprint. This is where the
front-end code goes to ask the bot something.
"""
from flask import Blueprint, jsonify, request
from grandma.bot import Query

API_BLUEPRINT = Blueprint('api',
                          __name__,
                          url_prefix='/api')

@API_BLUEPRINT.route('/query')
def query_endpoint():
    """
    The only endpoint of the API. You send the query
    via the query parameters, and you get JSON, with
    the address message in the address field, the
    staticmap in PNG (encoded in base64) in the staticmap
    field, the fact about the place in the funfact field,
    and any errors that have occured in the errors field.
    """
    query = Query(request.args.get("query"))

    return jsonify({
        "errors": query.errors,
        "error_message": query.error_message,
        
        "messages": getattr(query, "messages", None),
        "staticmap": getattr(query, "staticmap", None)
    })
