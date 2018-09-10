# -*- coding: utf-8 -*-

from six.moves import urllib

__all__ = ("Request",)

class Request(object):
    def __init__(self, environ):
        self.environ = environ

    @property
    def args(self):
        ''' 查询字符串 => dict() '''
        arguments = urllib.parse.parse_qs(
            self.environ["QUERY_STRING"]
        )
        return {k: v[0] for k, v in arguments.items()}

    @property
    def path(self):
        return self.environ["PATH_INFO"]
