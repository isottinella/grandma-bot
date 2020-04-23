# helpers_requests.py ---
#
# Filename: helpers_requests.py
# Author: Louise <louise>
# Created: Thu Apr 23 20:50:39 2020 (+0200)
# Last-Updated: Thu Apr 23 20:50:45 2020 (+0200)
#           By: Louise <louise>
#
import requests

def patch_requests_no_internet(monkeypatch):
    """
    This helper patches requests.get to behave as if
    there is no internet connection.
    """
    def failed_request(url, params = {}, **kw):
        raise requests.exceptions.ConnectionError

    monkeypatch.setattr(requests, "get", failed_request)

def patch_requests_assert_false(monkeypatch):
    """
    This function is useful to guarantee no requests is made.
    """
    def requests_get(url, params = {}, **kw):
        assert False

    monkeypatch.setattr(requests, "get", requests_get)
