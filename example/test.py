

def application(environ, start_response):
    from pprint import pprint
    pprint(environ)
    # from six.moves import urllib
    # request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    # form = urllib.parse.parse_qs(environ["wsgi.input"].read(request_body_size).decode("utf-8"))
    # print(form)
    # try:
    # except:
    #     pass
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello world']


if __name__ == '__main__':
    # from wsgiref.simple_server import make_server
    # # httpd = make_server("127.0.0.1", 8000, app)
    # httpd = make_server("127.0.0.1", 8000, application)
    # httpd.serve_forever()
    def func(a,b):
        pass
    print(func)
    print(func.__code__.co_varnames)
