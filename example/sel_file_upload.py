from yoi.application import Application
from yoi.globals import g
from yoi.response import file_resp
import hashlib

app = Application()


@app.router(r"^/$", r"^/home/?$", methods=["GET"])
def index():
    return file_resp('./file.html')


@app.router(r"^/upload/?$", methods=["POST"])
def upload():
    form = g["request"].form
    # print(request.file["name"])
    file = form["file"]
    data = file.file.read()
    file_name = hashlib.md5(data).hexdigest()
    with open("./files/" + file_name + "_" + file.filename, "wb") as f:
        f.write(data)
    return 'success'

# def show(filename):
#     pass


def gallery(page_num):
    pass


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
