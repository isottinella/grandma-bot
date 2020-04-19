# blueprint.py --- 
# 
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:53:26 2020 (+0200)
# Last-Updated: Sun Apr 19 12:36:00 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint, render_template, request, url_for

webapp_blueprint = Blueprint('webapp',
                   __name__,
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/',
                   url_prefix='')

@webapp_blueprint.route('/')
def index():
    return render_template("index.jinja2")
