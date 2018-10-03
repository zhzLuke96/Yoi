"""
Achieve a safe coroutine global variable operation, which is a relatively simplified ctx module in flask
"""
import asyncio

__all__ = ("localvars", "loc_proxy", "set_proxy")


class proscenium:
    """
    a class dict manager or dict proxy
    """

    def __init__(self, evloop):
        self.dicts = dict()
        self.evloop = evloop

    def current_coro_id(self):
        return hash(asyncio.Task.current_task(self.evloop))

    def current_hook(self, cb):
        task = asyncio.Task.current_task(self.evloop)
        if task:
            task.add_done_callback(cb)

    def get_dict(self):
        id = self.current_coro_id()
        return self.dicts[id]

    def create_dict(self):
        id = self.current_coro_id()
        new_dict = {}
        self.dicts[id] = new_dict

        def clean_cb(*args):
            self.clean_up_byid(id)
        self.current_hook(clean_cb)
        return new_dict

    def clean_up_byid(self, id):
        if self.dicts[id]:
            del self.dicts[id]


class localvars:
    """
    Coroutines-safe

    # updata: fix Coroutines-safe  -  localvars_1_180928

    py => magic
    """

    def __init__(self, loop=asyncio.get_event_loop()):
        object.__setattr__(self, "__manager__", proscenium(loop))

    def current_vars(self):
        man = object.__getattribute__(self, "__manager__")
        try:
            vars = man.get_dict()
        except:
            vars = man.create_dict()
        return vars

    def __get__(self):
        return object.__getattribute__(self, "current_vars")()

    def __setitem__(self, key, val):
        return object.__getattribute__(self, "current_vars")().__setitem__(key, val)

    def __getitem__(self, key):
        return object.__getattribute__(self, "current_vars")().__getitem__(key)

    def __delitem__(self, key):
        return object.__getattribute__(self, "current_vars")().__delitem__(key)

    def __getattribute__(self, name):
        return object.__getattribute__(self, "current_vars")().__getattribute__(name)

    def __setattr__(self, name, val):
        return object.__getattribute__(self, "current_vars")().__setattr__(name, val)

    def __delattr__(self, name):
        return object.__getattribute__(self, "current_vars")().__delattr__(name)


class loc_proxy:
    """
    Proxy object, its operation behavior will be mapped to target item of corresponding local object(Current coroutine)

    eg:
        app_ctx = localvars()
        request = loc_proxy(app_ctx, "request")
        session = loc_proxy(app_ctx, "session")
    """
    def __init__(self, ctx, key):
        object.__setattr__(self, "__ctx__", ctx)
        object.__setattr__(self, "__key__", key)

    def __proxy_obj__(self):
        ctx = object.__getattribute__(self, "__ctx__")
        local = object.__getattribute__(ctx, "__get__")()
        key = object.__getattribute__(self, "__key__")
        return dict.__getitem__(local, key)
        # return local[key]

    def __get__(self):
        return self.__proxy_obj__()

    def __set__(self, val):
        ctx = object.__getattribute__(self, "__ctx__")
        local = object.__getattribute__(ctx, "__get__")()
        key = object.__getattribute__(self, "__key__")
        return dict.__setitem__(local, key, val)

    def __setitem__(self, key, val):
        proxy = object.__getattribute__(self, "__proxy_obj__")()
        return proxy.__setitem__(key, val)

    def __getitem__(self, key):
        proxy = object.__getattribute__(self, "__proxy_obj__")()
        return proxy.__getitem__(key)

    def __delitem__(self, key):
        proxy = object.__getattribute__(self, "__proxy_obj__")()
        return proxy.__delitem__(key)

    def __getattribute__(self, name):
        proxy = object.__getattribute__(self, "__proxy_obj__")()
        return proxy.__getattribute__(name)

    def __setattr__(self, name, val):
        proxy = object.__getattribute__(self, "__proxy_obj__")()
        return proxy.__setattr__(name, val)

    def __delattr__(self, name):
        proxy = object.__getattribute__(self, "__proxy_obj__")()
        return proxy.__delattr__(name)


def set_proxy(proxy, val):
    """
    Set proxied object by '__set__' function instead of using dot
    """
    setter = object.__getattribute__(proxy, "__set__")
    return setter(val)
