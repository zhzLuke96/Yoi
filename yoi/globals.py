from .ctx import __ctx__stack
import time
from .utils import session_id, getId

__all__ = ("g",)

g = dict()
cookies = __ctx__stack()


class easy_Cache(dict):
    def __init__(self, MaxAge=3600):
        self.max_age = MaxAge

    def save(self, obj, id=getId()):
        self[id] = (obj, int(time.time()))
        return id

    def load(self, id, default=None):
        obj, t = self.get(id, (default, 0))
        if time.time() - t > self.max_age:
            try:
                self.pop(id)
            except:
                pass
        return obj

class _Session(object):
    def __init__(self, factory=easy_Cache(), id_string="_session_ID_"):
        self.factory = factory
        self.cookie_id = id_string

    @property
    def id(self):
        _id = cookies[self.cookie_id]
        if _id is None:
            _id = self.factory.save({})
            cookies[self.cookie_id] = _id
        return _id

    def new_ID(self):
        _id = self.factory.save({})
        cookies[self.cookie_id] = _id
        return _id

    @property
    def this(self):
        return self.factory.load(self.id)

    def __getitem__(self, key):
        return self.this[key]

    def __setitem__(self, key, val):
        self.this[key] = val


class server_session(object):
    def __init__(self, factory=easy_Cache()):
        self.factory = factory

    @property
    def id(self):
        if "environ" in g:
            _id = session_id(g["environ"])
            if _id not in self.factory:
                self.factory.save({}, _id)
            return _id
        else:
            return None

    @property
    def this(self):
        return self.factory.load(self.id)

    def __getitem__(self, key):
        return self.this[key]

    def __setitem__(self, key, val):
        self.this[key] = val


Session = _Session()
SSession = server_session()
