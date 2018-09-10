
from yoi.router import Router
from yoi.application import Application
from yoi.globals import cookies, Session, SSession

# router = Router()
app = Application()


def html(text):
    return f"""<!DOCTYPE html>
<html lang="en">
    <head></head>
    <body>
        {text}
        <br/>
        <span>client <=> server Session:
        <input style="width:300px;" type="search" name="user_search" value="{Session.id}" />
        </span>
        <br/>
        <span>server session:
        <input style="width:500px;" type="search" name="user_search" value="{SSession.id}" />
        </span>
    </body>
</html>"""


app.Router.add_static_folder("/", "./www/")


@app.Router(r"/hello/([^/]*)/?$", r"/he/([^/]*)/?$")
def hello(request, name):
    return html(f"<h1>hello {name}!</h1><br>{cookies['id']}")


@app.Router(r"/nihao/([^/]*)/?$")
def nihao(request, name):
    return html(f"<h1>nihao {name}!</h1>")


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
