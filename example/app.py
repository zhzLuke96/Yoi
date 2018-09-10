
from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    name = request.args.get("name","PyCon")
    return Response([f'<h1>hello {name}!</h1>'])


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    # httpd = make_server("127.0.0.1", 8000, app)
    httpd = make_server("127.0.0.1", 8000, application)
    httpd.serve_forever()
