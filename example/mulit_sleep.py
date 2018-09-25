from yoi.application import Application
import time

app = Application()


@app.router(r"^/sleep/(.+)/?$", methods=["GET"])
def index(request,timer):
    time.sleep(int(timer))
    return f"server sleep {timer}s"

@app.router(r"^/do/?$", methods=["GET"])
def index():
    return f"server do something"


if __name__ == '__main__':
    from yoi.server.sel_wsgiServer import WSGIServer

    sev = WSGIServer("127.0.0.1",8000).set_application(app)
    sev.run()

    # from wsgiref.simple_server import make_server
    # # httpd = make_server("127.0.0.1", 8000, app)
    # httpd = make_server("localhost", 8000, app)
    # try:
    #     httpd.serve_forever()
    # except:
    #     httpd.shutdown()
    #     raise
