import asyncio

__all__ = ("localvars",)


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
        return object.__getattribute__(self, "current_vars")

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
