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

    def add_router(self, pattern, callback, methods=["GET"]):
        self.routing_table.append((pattern, callback, methods))

    def add_static_folder(self, pattern, folder_name):
        if folder_name[-1] != "/":
            folder_name += "/"

        def _(request, file_path):
            if file_path is None or file_path == "":
                file_path = "index.html"
            try:
                file = open(folder_name + file_path, "rb")
                bin = file.read()
            except:
                raise NotFoundError()
            resp = Response(bin, content_type=mime_type(file_path))
            resp.add_header("Cache-Control", "public, max-age=31536000")
            return resp
        self.static_router.append((pattern + r"([\s\S]+)?$", _, ["GET"]))

    def match(self, path, method):
        table = [row for row in sorted(
            self.routing_table, key=lambda x: -x[0].count("/")) if method in row[2]]
        table += [row for row in sorted(
            self.static_router, key=lambda x: -x[0].count("/")) if method in row[2]]

        for p, c, _m in table:
            m = re.match(p, path)
            if m:
                return (c, m.groups())

        raise NotFoundError()

    def __call__(self, *args, methods=["GET"]):
        def _(func):
            for pattern in args:
                self.add_router(pattern, func, methods)
        return _
