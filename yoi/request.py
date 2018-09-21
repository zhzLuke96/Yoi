# -*- coding: utf-8 -*-

from six.moves import urllib
from .session import session_info, Session

__all__ = ("Request",)

session_key = "_session_ID_"


def ck_parse(ck_string):
    if len(ck_string) < 3 or "=" not in ck_string:
        return {"0": ck_string}
    rows = ck_string.split(";")
    res = {}
    for r in rows:
        k, v = r.split("=")
        res[k] = v
    return res


class Request(object):
    def __init__(self, environ, session_factroy):
        self.environ = environ
        self._form = None
        self._factroy = session_factroy
        self._session = None

    def get_forms(self, decoding="utf-8"):
        if self._form:
            return self._form
        try:
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
            arguments = urllib.parse.parse_qs(
                self.environ["wsgi.input"].read(request_body_size))
            self._form = {k.decode(decoding): v[0]
                          for k, v in arguments.items()}
        except:
            self._form = {}
        return self._form

    @property
    def args(self):
        ''' 查询字符串 => dict() '''
        arguments = urllib.parse.parse_qs(
            self.environ["QUERY_STRING"]
        )
        return {k: v[0] for k, v in arguments.items()}

    @property
    def form(self):
        ''' POST_BODY '''
        return self.get_forms()

    @property
    def cookies(self):
        ''' cookies '''
        return ck_parse(self.environ.get("HTTP_COOKIE", ""))

    @property
    def session(self):
        if self._session is None:
            _id = self.cookies.get(session_key, None)
            if _id is None or not self._factroy.is_alive(_id):
                s = Session()
                self._factroy.save(s, s.sid)
                self._session = s
            else:
                self._session = self._factroy.load(_id)
        return self._session

    @property
    def method(self):
        ''' GET|POST|PUT|DELETE|OPTIONS'''
        return self.environ.get("REQUEST_METHOD", "GET")

    @property
    def path(self):
        return self.environ.get("PATH_INFO", "")

    @property
    def user_info(self):
        return session_info(self.environ)
