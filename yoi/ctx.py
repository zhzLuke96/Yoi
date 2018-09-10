
__all__ = ("__ctx__stack",)


def ck_dict(ck_string):
    if len(ck_string) < 3 or "=" not in ck_string:
        return {"_c_": ck_string}
    rows = ck_string.split(";")
    res = {}
    for r in rows:
        k, v = r.split("=")
        res[k] = v
    return res


class __ctx__stack(object):
    def __init__(self):
        self._stack = []

    def push(self, val):
        self._stack.append(ck_dict(val))

    def pop(self):
        if len(self._stack) == 0:
            return None
        return self._stack.pop()

    @property
    def top(self):
        if len(self._stack) == 0:
            return None
        return self._stack[-1]

    def __getitem__(self, attr):
        if len(self._stack) == 0:
            return None
        return self._stack[-1].get(attr, None)

    def __setitem__(self, key, val):
        if len(self._stack) == 0:
            return None
        self._stack[-1][key] = val
