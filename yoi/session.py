__all__ = ("Session","session_info")


def session_info(environ):
    return {
        "ip": (environ.get("REMOTE_ADDR", ""), environ.get("REMOTE_HOST", "")),
        "agent": environ.get("HTTP_USER_AGENT", ())
    }


def hex36(num):
    key = '0123456789abcdefghijklmnopqrstuvwxyz'
    a = []
    while num >= 1:
        a.append(key[int(num % 36)])
        num = num / 36
    a.reverse()
    out = ''.join(a)
    return out


class Session(dict):
    @property
    def sid(self):
        return hex36(id(self))


if __name__ == '__main__':
    s1 = Session()
    s1["1"] = 1
    s2 = Session()
    s3 = Session()

    print(s1, s1.sid)
    print(s2, s2.sid)
    print(s3, s3.sid)
