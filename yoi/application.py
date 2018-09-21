from .request import Request
from .response import Response
from .router import NotFoundError, Router
from .utils import session_cookie_string
from .storage_factory import factory_simple

__all__ = ("Application",)


def call_warpper(callback, request, args):
    varnames = callback.__code__.co_varnames
    if varnames[0] == "request":
        return callback(request, *args)
    return callback(*args)


class Application(object):
    def __init__(self, Router=Router(), session_factroy=factory_simple(), **kwargs):
        self.Router = Router
        self.session_pool = session_factroy

    def __call__(self, environ, start_response):
        # from pprint import pprint; pprint(environ)

        try:
            request = Request(environ, self.session_pool)

            # updata globals value
            from .globals import g
            g["environ"] = environ
            g["request"] = request
            g["session"] = request.session

            # exec_match
            callback, args = self.Router.match(request.path, request.method)

            user_response = call_warpper(callback, request, args)
            # exec_match EOF

            response = user_response if isinstance(
                user_response, Response) else Response(user_response)
            response.add_header(
                'Set-Cookie', session_cookie_string(request.session.sid))
        except NotFoundError:
            response = Response("<h1>Not Found</h1>", status=404)
        # print(response.headers)
        start_response(response.status, response.headers.items())
        return iter(response)
