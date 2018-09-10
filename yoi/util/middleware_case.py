class UppercaseMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        for data in self.app(environ, start_response):
            yield data.upper()
