# --
# entry point
# --

from app import app
from app.main.yoi.server import aio_wsgiServer
# from config import debug_config

#  -----------------------------
#  config

port = 9527
addr = "127.0.0.1"

#  -----------------------------
#  main

if __name__ == '__main__':
    print(f"server on {addr}:{port}")
    sev = aio_wsgiServer.WSGIServer(app, addr, port)
    sev.set_chunk_size(5242880)
    # *one chunk size 5mb, default size is 1024B
    sev.run_forever()
