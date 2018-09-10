# -*- coding: utf-8 -*-
import datetime
import random
import hashlib

__all__ = ("session_id", "session_cookie_string", "getId")


def hex36(num):
    key = '0123456789abcdefghijklmnopqrstuvwxyz'
    a = []
    while num >= 1:
        a.append(key[int(num % 36)])
        num = num / 36
    a.reverse()
    out = ''.join(a)
    return out


def getId():
    d2 = datetime.datetime.now()
    ms = d2.microsecond
    id1 = hex36(random.randint(36, 10000))
    id2 = hex36(random.randint(36, 10000))
    id3 = hex36(ms + 46656)

    mId = id1 + id3 + id2
    return mId[::-1]


Query_String = {
    "http_mothod": "REQUEST_METHOD",
    "user_ip": "REMOTE_ADDR",
    "user_agent": "HTTP_USER_AGENT",
}


def session_id(environ):
    q_s = ""
    if Query_String["user_ip"] in environ:
        q_s += environ[Query_String["user_ip"]]
    if Query_String["user_agent"] in environ:
        q_s += environ[Query_String["user_agent"]]
    return hashlib.sha1(q_s.encode("utf-8")).hexdigest()


def session_cookie_string(id, cookie_key='_session_ID_'):
    try:
        from Cookie import SimpleCookie
    except ImportError:
        from http.cookies import SimpleCookie
    cookie = SimpleCookie()
    cookie[cookie_key] = id
    cookie[cookie_key]['path'] = '/'
    return cookie[cookie_key].OutputString()
