from .utils import getId
import time


class factory_simple(dict):
    def __init__(self, MaxAge=3600):
        self.max_age = MaxAge

    def is_alive(self, id):
        obj, t = self.get(id, (None, 0))
        if time.time() - t > self.max_age:
            return False
        return True

    def save(self, obj, id=getId()):
        self[id] = (obj, int(time.time()))
        return id

    def load(self, id):
        if self.is_alive(id):
            return self.get(id, (None,None))[0]
        return None
