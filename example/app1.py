
from yoi.router import Router
from yoi.application import Application
from yoi.globals import g

# router = Router()
app = Application()


def html(text):
    return f"""<!DOCTYPE html>
<html lang="en">
    <head></head>
    <body>
        {text}
        <span>server session:
        <input style="width:500px;" type="search" name="user_search" value="{g["session"].sid}" />
        </span>
    </body>
</html>"""


app.Router.add_static_folder("/", "./www/")


@app.Router(r"/hello/([^/]*)/?$", r"/he/([^/]*)/?$")
def hello(name):
    request = g["request"]
    # print("request")
    from pprint import pprint
    pprint(request.__dict__)
    return html(f"<h1>hello {name}!</h1><br>{cookies['id']}")


@app.Router(r"/nihao/([^/]*)/?$")
def nihao(name):
    request = g["request"]
    tail = request.args.get("tail", "none-tail")
    print("request.args", request.args)
    print("request.cookies", request.cookies)
    print("request.session", request.session)
    print("request.form", request.form)

    return html(f"<h1>nihao {name}! [{tail}]</h1>")


@app.Router(r"/calc/?$", methods=["POST"])
def calc_model(request):
    form = request.form
    return str(int(form["b"]) + int(form["w"]) * int(form["x"]))

# app = Application(Router=router)
# app = UppercaseMiddleware(app)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    # httpd = make_server("127.0.0.1", 8000, app)
    httpd = make_server("localhost", 8000, app)
    try:
        httpd.serve_forever()
    except:
        httpd.shutdown()
        raise
