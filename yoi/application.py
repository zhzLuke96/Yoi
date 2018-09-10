from .request import Request
from .response import Response
from .router import NotFoundError, Router
from .utils import session_cookie_string

__all__ = ("Application",)
# __all__ = ("yoi_appliction", "Application",)


def yoi_appliction(func):
    def appliction(environ, start_response):
        request = Request(environ)
        user_response = func(request)
        response = user_response if isinstance(
            user_response, Response) else Response(user_response)

        start_response(
            response.status,
            response.headers.items()
        )
        return iter(response)
    return appliction


class Application(object):
    def __init__(self, Router=Router(), **kwargs):
        self.Router = Router

    def __call__(self, environ, start_response):
        # print(environ)
        try:
            request = Request(environ)
            from .globals import cookies, Session, g
            g["environ"] = environ
            if 'HTTP_COOKIE' in environ:
                cookies.push(environ['HTTP_COOKIE'])
            s_id = Session.id

            # exec_match
            callback, args = self.Router.match(request.path)
            user_response = callback(request, *args)
            # exec_match EOF

            if 'HTTP_COOKIE' in environ:
                cookies.pop()
            response = user_response if isinstance(
                user_response, Response) else Response(user_response)
            response.add_header('Set-Cookie', session_cookie_string(s_id))
        except NotFoundError as e:
            response = Response("<h1>Not Found</h1>", status=404)
        start_response(response.status, response.headers.items())
        return iter(response)
