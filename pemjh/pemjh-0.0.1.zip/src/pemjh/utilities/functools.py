""" Function tools """
from __future__ import absolute_import
from functools import wraps


def memoize(func):
    cache = {}

    @wraps(func)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoizer
