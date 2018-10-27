# coding: utf-8
from __future__ import unicode_literals

import asyncio
from io import StringIO, BytesIO
import sys
import datetime
import platform

import h11

__version__ = '0.2'

__all__ = ("WSGIServer",)


def _partition_header(stream):
    return stream.split(b'\r\n\r\n')[0]


class WSGIServer(object):
    server_version = "asyncWSGIServer/" + __version__
    server_platform = "Python/" + platform.python_version()

    # 5mb
    recv_buff_size = 65535

    def __init__(self, app, host, port, loop=asyncio.get_event_loop()):
        self.application, self.host, self.port = app, host, port
        self.loop = loop
        self.chunk_size = None

    def set_chunk_size(self, val):
        self.chunk_size = val
        return self

    def run_forever(self):
        coro = asyncio.start_server(
            self.handle_sev, self.host, self.port, loop=self.loop)
        server = self.loop.run_until_complete(coro)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            # Close the server
            server.close()
            self.loop.run_until_complete(server.wait_closed())
            self.loop.close()

    def logging(self, addr, info, status, res_length=0):
        print ('{3} -- [{0}] "{1}" {2} {4}'.format(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), info, status, str(addr[0]) + ":" + str(addr[1]), res_length))

    async def handle_sev(self, reader, writer):
        chunk_size = self.chunk_size if self.chunk_size is not None else self.recv_buff_size
        empty_bytes = b''
        data = empty_bytes
        while True:
            chunk = await reader.read(chunk_size)
            await asyncio.sleep(0.05)
            # switch coro
            data += chunk
            if data.count(b"WebKitFormBoundary") != 0 and data[-4:] != b"--\r\n":
                continue
            if len(chunk) < chunk_size:
                break
        message = _partition_header(data).decode()
        addr = writer.get_extra_info('peername')
        # print("Received %r from %r" % (message, addr)
        app_data, info = await self._on_read(data, addr)
        resp = self._on_write(app_data, info[1], info[0])

        self.logging(addr, message.splitlines()[0], info[0], len(resp))

        writer.write(resp.encode("utf-8"))
        await writer.drain()
        # print("Close the client socket")
        writer.close()

    async def _on_read(self, data, addr):
        lines = _partition_header(data).decode().splitlines()
        request = self.get_url_parameter(lines)
        env = self.get_environ(request, data, addr)
        start, ret = self.start_response()
        app_data = await self.application.async_call(
            env, start)
        status, header = ret()
        return app_data, (status, header)

    def _on_write(self, app_data, headers, status):
        """=== finish_response"""
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)
        for header in headers:
            response += '{0}: {1}\r\n'.format(*header)
        response += '\r\n'
        for data in app_data:
            response += data if isinstance(data, str) else data.decode()
        return response

    def get_url_parameter(self, request_lines):
        request_dict = {'Path': request_lines[0]}
        for itm in request_lines[1:]:
            if ':' in itm:
                request_dict[itm.split(':')[0]] = itm.split(':')[1]
        return request_dict

    def get_environ(self, request_dict, request_data, addr):
        request_method, path, request_version = request_dict.get(
            'Path').split()
        if '?' in path:
            path, query = path.split('?', 1)
        else:
            path, query = path, ''
        env = {
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'SERVER_SOFTWARE': self.server_version,
            'SERVER_NAME': "*",
            'GATEWAY_INTERFACE': 'CGI/1.1',
            'REMOTE_ADDR': addr[0],
            'REMOTE_HOST': addr[1],
            'SCRIPT_NAME': '',
            # ....
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': BytesIO(request_data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': request_method,
            'QUERY_STRING': query,
            'PATH_INFO': path,
            'SERVER_NAME': self.host,
            'SERVER_PORT': self.port,
            'CONTENT_TYPE': request_dict.get('Content-Type', 'text/plain'),
            'CONTENT_LENGTH': request_dict.get('Content-Length', '')
        }
        for k, v in request_dict.items():
            k = k.replace('-', '_').upper()
            v = v.strip()
            if k in env:
                # cover (skip) content length, type,etc.
                env[k] = v
            if 'HTTP_' + k in env:
                # comma-separate multiple headers
                env['HTTP_' + k] += ',' + v
            else:
                env['HTTP_' + k] = v
        return env

    def start_response(self):
        res_headers = [
            ('Date', datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')),
            ('Server', self.server_version + ' ' + self.server_platform),
        ]
        res_status = None

        def setted():
            return res_status, res_headers

        def _start(status, response_headers):
            nonlocal res_status
            nonlocal res_headers
            res_headers = response_headers + res_headers
            res_status = status

        return _start, setted

# --------
# demo app

async def application(environ, start_response):
    # import time
    # time.sleep(10)
    # await asyncio.sleep(10)
    # from pprint import pprint;pprint(environ)
    response_body = 'The request method was %s' % environ['REQUEST_METHOD'] + \
        "\n\r" + datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

if __name__ == '__main__':
    wsgi = WSGIServer(application, "127.0.0.1", 8888)
    wsgi.run_forever()
