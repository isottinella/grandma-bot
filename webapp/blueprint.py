# blueprint.py --- 
# 
# Filename: blueprint.py
# Author: Louise <louise>
# Created: Sat Apr 18 18:53:26 2020 (+0200)
# Last-Updated: Sat Apr 18 18:59:07 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint, render_template

webapp = Blueprint('webapp',
                   __name__,
                   template_folder='templates',
                   url_prefix='')

@webapp.route('/')
def index():
    return render_template("index.jinja2")
