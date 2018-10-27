# --
# entry point
# --

from app import app
# from config import debug_config

if __name__ == '__main__':
    from yoi.server import sel_wsgiServer

    port = 9527
    sev = aio_wsgiServer.WSGIServer(app, "127.0.0.1", port)
    print(f"server on 127.0.0.1:{port}")
    sev.run_forever()

    # from wsgiref.simple_server import make_server
    # # httpd = make_server("127.0.0.1", 8000, app)
    # httpd = make_server("localhost", 8000, app)
    # try:
    #     httpd.serve_forever()
    # except:
    #     httpd.shutdown()
    #     raise
