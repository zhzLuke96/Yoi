from yoi.application import Application
import time
import asyncio
import datetime
import platform

app = Application()


@app.router(r"^/sleep/(.+)/?$", methods=["GET"])
async def index(request, timer):
    time.sleep(int(timer))
    return f"server sleep {timer}s \n {datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}"


@app.router(r"^/aiosleep/(.+)/?$", methods=["GET"])
async def index(timer):
    await asyncio.sleep(int(timer))
    return f"server async sleep {timer}s \n {datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}"


@app.router(r"^/do/?$", methods=["GET"])
async def index():
    return f"server do something"

@app.errorhandler("404")
def not_found():
    return f"<h1>Not Found 404</h1><p>server on {platform.python_version()}</p>"


if __name__ == '__main__':
    from yoi.server.aio_wsgiServer import WSGIServer

    sev = WSGIServer(app, "127.0.0.1", 8000)
    sev.run_forever()

    # from wsgiref.simple_server import make_server
    # # httpd = make_server("127.0.0.1", 8000, app)
    # httpd = make_server("localhost", 8000, app)
    # try:
    #     httpd.serve_forever()
    # except:
    #     httpd.shutdown()
    #     raise
