from .request import Request
from .response import Response
from .router import NotFoundError, Router
from .utils import session_cookie_string
from .storage_factory import factory_simple

__all__ = ("Application",)


def call_warpper(callback, request, args):
    """
    change the calling policy according to the parameters of callback function
    *beautiful code ,oopssssssss
    """
    varnames = callback.__code__.co_varnames
    argcount = callback.__code__.co_argcount
    if argcount != 0 and varnames[0] == "request":
        return callback(request, *args)
    return callback(*args)


def updata_localvars(environ, cur_request):
    """
    ctx__local power by asyncio_current_task XD
    """
    from .globals import g, request_setter, session_setter
    g["environ"] = environ
    g["request"] = cur_request
    # object.__set__(request,cur_request)
    request_setter(cur_request)
    g["session"] = cur_request.session
    # session = cur_request.session
    session_setter(cur_request.session)


class Application(object):
    """
    wsgi application class
    """
    def __init__(self, router=Router(), session_factroy=factory_simple(), config=dict(), **kwargs):
        self.router = router
        self.session_pool = session_factroy
        # self.config = config
        self._error_resp_table = dict(default="<h1>Not Found</h1>")
        # set_globals("config", config)

    def errorhandler(self, status_code):
        def _(fn):
            self._error_resp_table[f"{status_code}"] = fn
        return _

    async def async_call(self, environ, start_response):
        request = Request(environ, self.session_pool)
        # updata globals value
        updata_localvars(environ, request)
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
            msg = self._error_resp_table.get(
                "404", self._error_resp_table["default"])
            if callable(msg):
                msg = msg()
            response = Response(msg, status=404)
        # print(response.headers)
        start_response(response.status, response.headers.items())
        return iter(response)

    def __call__(self, environ, start_response):
        """
        * for compatibility retention methods, if code review, you can skip this paragraph at willf.
        """

        request = Request(environ, self.session_pool)
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
            msg = self._error_resp_table.get(
                "404", self._error_resp_table["default"])
            if callable(msg):
                msg = msg()
            response = Response(msg, status=404)
        # print(response.headers)
        start_response(response.status, response.headers.items())
        return iter(response)
