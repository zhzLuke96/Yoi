from .localvars import localvars, loc_proxy

__all__ = ("g", "request", "session")

g = localvars()
app_ctx = localvars()
request = loc_proxy(app_ctx, "request")
session = loc_proxy(app_ctx, "session")
