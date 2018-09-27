from .request import Request
from .response import Response
from .router import NotFoundError, Router
from .utils import session_cookie_string
from .storage_factory import factory_simple

__all__ = ("Application",)


def call_warpper(callback, request, args):
    varnames = callback.__code__.co_varnames
    argcount = callback.__code__.co_argcount
    if argcount != 0 and varnames[0] == "request":
        return callback(request, *args)
    return callback(*args)


def set_globals(key, value):
    from .globals import g
    g[key] = value


class Application(object):
    def __init__(self, router=Router(), session_factroy=factory_simple(), config=dict(), **kwargs):
        self.router = router
        self.session_pool = session_factroy
        self.config = config
        self._error_resp_table = dict(default="<h1>Not Found</h1>")
        set_globals("config", config)

    def errorhandler(self, status_code):
        def _(fn):
            self._error_resp_table[f"{status_code}"] = fn
        return _

    async def async_call(self, environ, start_response):
        request = Request(environ, self.session_pool)
        # updata globals value
        set_globals("environ", environ)
        set_globals("request", request)
        set_globals("session", request.session)
        try:
            # exec_match
            callback, args = self.router.match(request.path, request.method)

            user_response = await call_warpper(callback, request, args)
            # exec_match EOF

            response = user_response if isinstance(
                user_response, Response) else Response(user_response)
            response.add_header(
                'Set-Cookie', session_cookie_string(request.session.sid))
        except NotFoundError:
            msg = self._error_resp_table.get("404",self._error_resp_table["default"])
            if callable(msg):
                msg = msg()
            response = Response(msg ,status=404)
        # print(response.headers)
        start_response(response.status, response.headers.items())
        return iter(response)

    def __call__(self, environ, start_response):
        # from pprint import pprint; pprint(environ)

        request = Request(environ, self.session_pool)
        # updata globals value
        set_globals("environ", environ)
        set_globals("request", request)
        set_globals("session", request.session)
        try:
            # exec_match
            callback, args = self.router.match(request.path, request.method)

            user_response = call_warpper(callback, request, args)
            # exec_match EOF

            response = user_response if isinstance(
                user_response, Response) else Response(user_response)
            response.add_header(
                'Set-Cookie', session_cookie_string(request.session.sid))
        except NotFoundError:
            msg = self._error_resp_table.get("404",self._error_resp_table["default"])
            if callable(msg):
                msg = msg()
            response = Response(msg ,status=404)
        # print(response.headers)
        start_response(response.status, response.headers.items())
        return iter(response)
