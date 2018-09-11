
from yoi.router import Router
from yoi.response import Response, Redirect_resp
from yoi.application import Application
from yoi.globals import cookies, Session, SSession, g

from datetime import datetime

# router = Router()
app = Application()

g["posts"] = []

@app.Router(r"/?$")
def index(request):
    return Redirect_resp("/home/")

@app.Router(r"/post/?$")
def post(request):
    content = request.args.get("content", None)
    print("new post ====>>> ",content)
    if content is not None:
        g["posts"].append((Session.id, str(datetime.now())[:-7], content))
    resp = Redirect_resp("/home/")
    # get method is cached with defult
    resp.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    return resp


def html():
    def base(h):
        return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><title> -|"'Board'"|- </title></head><body>{h}</body></html>"""

    def lis():
        res = ""
        for p in g["posts"]:
            res += f"<li><b>{p[0]}</b>_<small>{p[1]}</small>_<p>{p[2]}</p></li>"
        return res
    return base(f"""<form action="/post" method="get">content: <input type="text" name="content" /><input type="submit" value="Submit" /></form><br><ul>{lis()}</ul>""")


@app.Router(r"/home/?$")
def home(request):
    return html()


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
