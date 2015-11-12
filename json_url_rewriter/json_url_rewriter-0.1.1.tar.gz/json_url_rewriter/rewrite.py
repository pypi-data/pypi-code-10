import re

def get_by_key(doc, key):
    parts = key.split('.')
    ctx = doc
    try:
        for part in parts:
            ctx = ctx[part]
        return ctx
    except KeyError:
        return None


def set_by_key(doc, key, value):
    parts = key.split('.')
    path, target = parts[:-1], parts[-1]
    ctx = doc
    try:
        for part in path:
            ctx = ctx[part]
        if target not in ctx:
            raise KeyError
        ctx[target] = value
    except KeyError:
        pass
    return doc


class URLRewriter(object):
    def __init__(self, keys, regex=None, replacement=None):
        self.keys = keys
        self.regex = regex
        if self.regex:
            self.regex = re.compile(self.regex)
        self.replacement = replacement

    def rewrite(self, url):
        return self.regex.sub(self.replacement, url)

    def __call__(self, doc):
        for key in self.keys:
            url = get_by_key(doc, key)
            set_by_key(doc, key, self.rewrite(url))
        return doc
