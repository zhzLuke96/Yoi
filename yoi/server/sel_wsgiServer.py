# server.py
# coding: utf-8
from __future__ import unicode_literals

import socket
# import StringIO
from io import StringIO
import sys
import datetime
import selectors

__all__ = ("WSGIServer",)

class EventLoop:

    def __init__(self, selector=None):
        if selector is None:
            selector = selectors.DefaultSelector()
        self.selector = selector

    def run_forever(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    callback = key.data
                    callback(key.fileobj)
                else:
                    callback, app_data, headers, status = key.data
                    callback(key.fileobj, app_data, headers, status)


class WSGIServer(object):
    request_queue_size = 128
    recv_buff_size = 1024

    def __init__(self, host, port, loop=EventLoop()):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self._loop = loop

    def _accept(self, sock):
        conn, addr = sock.accept()
        # print('accepted', conn, 'from', addr)
        # print("_accept!")
        conn.setblocking(False)
        self._loop.selector.register(conn, selectors.EVENT_READ, self._on_read)

    def _on_read(self, conn):
        # print("_on_read!")
        recv_data = conn.recv(self.recv_buff_size).decode()
        lines = recv_data.splitlines()
        if not recv_data:
            print('closing', conn)
            self._loop.selector.unregister(conn)
            conn.close()
        try:
            request = self.get_url_parameter(lines)
            env = self.get_environ(request, recv_data)
            start_response, call_sel = self.start_response(conn, env)
            app_data = self.application(
                env, start_response)
            call_sel(app_data)
            # self._loop.selector.modify(conn, selectors.EVENT_WRITE, (self._on_write, app_data))
        except Exception as e:
            print(e)

    def _on_write(self, conn, app_data, headers, status):
        """=== finish_response"""
        # print("finish_response!")
        # print(list(app_data))
        try:
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in app_data:
                response += data if isinstance(data,str) else data.decode()
            conn.sendall(response.encode())
            self._loop.selector.modify(
                conn, selectors.EVENT_READ, self._on_read)
        finally:
            self._loop.selector.unregister(conn)
            conn.close()

    def run(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(self.request_queue_size)
        self.s.setblocking(False)
        self._loop.selector.register(
            self.s, selectors.EVENT_READ, self._accept)
        self._loop.run_forever()

    def set_application(self, application):
        self.application = application
        return self

    def get_url_parameter(self, request_lines):
        request_dict = {'Path': request_lines[0]}
        for itm in request_lines[1:]:
            if ':' in itm:
                request_dict[itm.split(':')[0]] = itm.split(':')[1]
        # request_method, path, request_version = request_dict.get(
        #     'Path').split()
        return request_dict

    def get_environ(self, request_dict, request_data):
        request_method, path, request_version = request_dict.get(
            'Path').split()
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO(request_data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': request_method,
            'PATH_INFO': path,
            'SERVER_NAME': self.host,
            'SERVER_PORT': self.port,
            'USER_AGENT': request_dict.get('User-Agent')
        }
        return env

    def start_response(self, conn, env):
        res_headers = [
            ('Date', datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')),
            ('Server', 'RAPOWSGI0.1'),
        ]
        res_status = None

        def call_select(app_data):
            # nonlocal self
            nonlocal conn
            nonlocal res_status
            nonlocal res_headers
            nonlocal env
            print ('[{0}] "{1}" {2}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            env.get("PATH_INFO","None"), res_status))
            self._loop.selector.modify(
                conn, selectors.EVENT_WRITE, (self._on_write, app_data, res_headers, res_status))

        def _start(status, response_headers):
            nonlocal res_status
            nonlocal res_headers
            res_headers = response_headers + res_headers
            res_status = status


        return _start, call_select

        # self._loop.selector.modify(conn, selectors.EVENT_WRITE, (self._on_write, msg))


def application(environ, start_response):
    # import time
    # time.sleep(10)
    response_body = 'The request method was %s' % environ['REQUEST_METHOD'] + "\n\r" + datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]


if __name__ == '__main__':
    port = 8888
    httpd = WSGIServer('127.0.0.1', int(port)).set_application(application)
    httpd.run()
