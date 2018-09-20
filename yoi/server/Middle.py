# coding: utf-8
# middleware.py
from __future__ import unicode_literals


class TestMiddle(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        if 'postman' in environ.get('USER_AGENT'):
            start_response('403 Not Allowed', [])
            return ['not allowed!']
        if "curl" in environ.get('USER_AGENT'):
            res = self.application(environ, start_response)
            return ["call from curl:\t"] + res
        return self.application(environ, start_response)
