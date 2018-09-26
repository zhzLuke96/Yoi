# Yoi
Asynchronous HTTP server framework for asyncio(come soon) and Python

# todo
- [x] router.wrapper
- [x] router.static_folder
- [x] globals.cookies
- [x] globals.session
- [x] globals.server_session (ip_agent)
- [x] better globals
- [x] better session (httponly max-age)
- [x] more_method: post put del...
- [x] wsgi_Server
- [x] asyncio_server
- [ ] asyncio_appliction
- [ ] mimetype_waring
- [ ] more_Type: json
- [ ] router for varnames
- [ ] cache_setting
- [ ] cache_response

> log 18/9/26:
> <br>asyncio server done.
> <br>


# asyncio
come soon..

# example
```python
# router = Router()
app = Application()

g["posts"] = []

@app.Router(r"/?$", methods = ["GET"])
def index():
    return Redirect_resp("/home/")

@app.Router(r"/post/?$", methods = ["POST"])
def post(request):
    content = request.args.get("content", None)
    if content is not None:
        g["posts"].append((g["session"].sid, str(datetime.now())[:-7], content))
    return "post success!"

def html():
    # ...

@app.Router(r"/home/?$")
def home(request):
    return html()

```

# 后
想融合flask和aiohttp于是写了这个东西(其实是练手作...)
