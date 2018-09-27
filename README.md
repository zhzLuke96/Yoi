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
- [x] asyncio_appliction
- [x] errorhandler
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

@app.Router(r"/?$", r"/home/?$")
async def index():
    return file_resp('./index.html')

@app.Router(r"/login/?$", methods = ["GET","POST"])
async def login(request):
    if request.method is "GET":
        name = request.args["name"]
        tags = request.args["tags"]
    else:
        name = request.from["name"]
        tags = request.from["tags"]
    g["online"][g["session"].sid](str(datetime.now())[:-7], (name,tags))
    # return f"<h1>hello {name}!</h1><p>you like: {tags}</p>"
    return "success"


@app.Router(r"/delay_exit/?$")
async def delay_exit():
    await asyncio.sleep(60)
    del g["online"][g["session"].sid]
    return "success"

@app.errorhandler("404")
def not_found():
    return f"<h1>Not Found 404</h1><p>server on {platform.python_version()}</p>"

```

# 后
想融合flask和aiohttp于是写了这个东西

more 2 [aioWebpy](https://www.github.com/zhzluke96)
