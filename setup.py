# setup.py --- 
# 
# Filename: setup.py
# Author: Louise <louise>
# Created: Sun Apr 19 02:43:49 2020 (+0200)
# Last-Updated: Fri Apr 24 00:24:04 2020 (+0200)
#           By: Louise <louise>
# 
from setuptools import setup

setup(
    name='grandma',
    packages=['grandma'],
    version="1.0",
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ],
)
