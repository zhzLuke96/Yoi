# -*- coding: utf-8 -*-

from six.moves import urllib
from .session import session_info, Session
from cgi import FieldStorage

__all__ = ("Request",)

session_key = "_session_ID_"


def _to_unicode(s, encoding='utf-8'):
    if isinstance(s, str):
        return s
    return s.decode('utf-8')


class MultipartFile(object):
    def __init__(self, storage):
        self.filename = _to_unicode(storage.filename)
        self.file = storage.file


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
        self._environ = environ
        self._fs = None
        self._form = None
        self._factroy = session_factroy
        self._session = None

    def _parse_input(self):
        def _convert(item):
            if isinstance(item, list):
                return [_to_unicode(i.value) for i in item]
            if item.filename:
                return MultipartFile(item)
            return _to_unicode(item.value)
        fs = FieldStorage(
            fp=self._environ['wsgi.input'], environ=self._environ, keep_blank_values=True)
        self._fs = fs
        inputs = {}
        for key in fs:
            inputs[key] = _convert(fs[key])
        self._form = inputs
        return inputs

    @property
    def args(self):
        ''' 查询字符串 => dict() '''
        arguments = urllib.parse.parse_qs(
            self._environ["QUERY_STRING"]
        )
        return {k: v[0] for k, v in arguments.items()}

    @property
    def form(self):
        ''' POST_BODY '''
        if self._form is not None:
            return self._form
        return self._parse_input()

    @property
    def cookies(self):
        ''' cookies '''
        return ck_parse(self._environ.get("HTTP_COOKIE", ""))

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
        return self._environ.get("REQUEST_METHOD", "GET")

    @property
    def path(self):
        return self._environ.get("PATH_INFO", "")

    @property
    def user_info(self):
        return session_info(self._environ)
