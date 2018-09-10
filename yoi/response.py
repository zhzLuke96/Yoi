from http.client import responses as HTTPCODE
from six.moves import urllib
from wsgiref.headers import Headers

__all__ = ("Response", "mime_type",)


def mime_type(fileName):
    import re
    from .util.mime_type import mimeType
    return mimeType.get("." + re.match(r".+\.(.+)$", fileName, re.I).group(1), 'application/octet-stream')


class Response(object):
    def __init__(self, response=None, status=200, charset='utf-8', content_type='text/plain'):
        self.response = [] if response is None else response
        self.charset = charset
        self.headers = Headers()
        content_type = f"{content_type}; charset={charset}"
        self.headers.add_header('content_type', content_type)
        self._status = status

    def add_header(self, key, val):
        self.headers.add_header(key, val)

    @property
    def status(self):
        status_string = HTTPCODE.get(self._status, 'UNKOWN STATUS')
        return f"{self._status} {status_string}"

    def __iter__(self):
        if isinstance(self.response, bytes):
            yield self.response
        else:
            yield self.response.encode(self.charset)
            # for val in self.response:
            #     yield val if isinstance(val, bytes) else val.encode(self.charset)


if __name__ == '__main__':
    print(HTTPCODE.get(200))
    print(HTTPCODE.get(500))
    print(HTTPCODE.get(400))
    print(HTTPCODE.get(300))
    TEST1 = Response("<h1>Hello!</h1>")
    print(list(iter(TEST1)))
    print(TEST1.status)
    print(TEST1.headers)
