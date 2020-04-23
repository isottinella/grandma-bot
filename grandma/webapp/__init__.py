# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:50:08 2020 (+0200)
# Last-Updated: Thu Apr 23 17:49:25 2020 (+0200)
#           By: Louise <louise>
#
"""
This module is there for everything front-end related.
It sends the template and all static assets.
"""
from flask import Blueprint, render_template

WEBAPP_BLUEPRINT = Blueprint('webapp',
                             __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/',
                             url_prefix='')

@WEBAPP_BLUEPRINT.route('/')
def index():
    """The index. Returns the main and only template."""
    return render_template("index.jinja2")
