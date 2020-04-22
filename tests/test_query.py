# test_query.py --- 
# 
# Filename: test_query.py
# Author: Louise <louise>
# Created: Tue Apr 21 18:57:33 2020 (+0200)
# Last-Updated: Thu Apr 23 01:32:58 2020 (+0200)
#           By: Louise <louise>
# 
from grandma.bot import Query

class TestQuery:
    def test_purify_query(self):
        pure = Query.purify_query("salut grandma, est-ce que tu sais "
                           "quelle est l'adresse d'openclassrooms")
        assert pure == "openclassrooms"
