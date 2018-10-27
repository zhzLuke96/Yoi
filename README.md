# Yoi
Asynchronous HTTP server framework for asyncio and Python

# todo
- [x] router.wrapper
- [x] router.static_folder
- [x] globals.cookies
- [x] globals.session
- [x] ~~globals.server_session (ip_agent)~~
- [x] better globals
- [x] better session (httponly max-age)
- [x] more_method: post put del...
- [x] wsgi_Server
- [x] asyncio_server
- [x] asyncio_appliction
- [x] errorhandler
- [x] safe_context => g,request,session(not ctx_stack)
- [x] localvars_proxy Class => request,session
- [x] aio_multipart
- [ ] better g & config
- [ ] config reader
- [ ] more_Type: json
- [ ] router for varnames
- [ ] cache_setting
- [ ] cache_response
- [ ] ~~aiohttp_lite~~
- [ ] ~~mimetype_waring~~

> log 18/10/28:
> <br>bug gone.
> <br>

# example
```python
from yoi.application import Application
from yoi.globals import g, request, session
app = Application()

online_table = dict()

@app.Router(r"/?$", r"/home/?$")
async def index():
    return file_resp('./index.html')

@app.Router(r"/login/?$", methods = ["GET","POST"])
async def login():
    if request.method is "GET":
        name = request.args["name"]
        tags = request.args["tags"]
    else:
        name = request.from["name"]
        tags = request.from["tags"]
    online_table[session.sid](str(datetime.now())[:-7], (name,tags))
    return "success"


@app.Router(r"/delay_exit/?$")
async def delay_exit():
    await asyncio.sleep(60)
    del online_table[session.sid]
    return "success"

@app.errorhandler("404")
def not_found():
    return f"<h1>Not Found 404</h1><p>server on {platform.python_version()}</p>"

if __name__ == '__main__':
    from yoi.server.aio_wsgiServer import WSGIServer
    sev = WSGIServer(app, "localhost", 8000)
    sev.run_forever()

```

# 后
想融合flask和aiohttp于是写了这个东西

next wait [aioWebpy](https://www.github.com/zhzluke96)

> 如果你正在写一个web应用，你可能会需要[这个](https://github.com/zhzLuke96/jsonflow)
> <br>像graphql一样写应用(雾)
