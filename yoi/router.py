import re
from .response import Response, mime_type

__all__ = ("NotFoundError", "Router")



class NotFoundError(Exception):
    """ url pattern not found"""
    pass


class Router(object):
    def __init__(self):
        self.routing_table = []
        self.static_router = []

    def add_router(self, pattern, callback):
        self.routing_table.append((pattern, callback))

    def add_static_folder(self, pattern, folder_name):
        def _(request, file_path):
            if file_path is None or file_path == "":
                file_path = "index.html"
            try:
                file = open(folder_name + file_path, "rb")
                bin = file.read()
            except:
                raise NotFoundError()
            return Response(bin, content_type=mime_type(file_path))
        self.static_router.append((pattern + r"([\s\S]+)?$", _))

    def match(self, path):
        table = sorted(self.static_router + self.routing_table,
                       key=lambda x: -len(x[0]))

        for p, c in table:
            m = re.match(p, path)
            if m:
                return (c, m.groups())

        raise NotFoundError()

    def __call__(self, *args):
        def _(func):
            for pattern in args:
                self.add_router(pattern, func)
        return _
