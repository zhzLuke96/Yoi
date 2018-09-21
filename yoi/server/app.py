def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    # print(environ)
    start_response(status, response_headers)
    return ['Hello world',]
