"""
    Defines all the global objects that are proxies to the current context(coroutine).

    todo:
    object g,Logically speaking, it should be independent of coroutine event loop, and applications often need a config class to set custom global objects (like other frameworks), and now g is obviously not the case...
"""
from .localvars import localvars, loc_proxy, set_proxy

__all__ = ("g", "request", "session", "request_setter", "session_setter")

g = localvars()
app_ctx = localvars()
request = loc_proxy(app_ctx, "request")
session = loc_proxy(app_ctx, "session")


def request_setter(val):
    global request
    return set_proxy(request, val)


def session_setter(val):
    global session
    return set_proxy(session, val)
