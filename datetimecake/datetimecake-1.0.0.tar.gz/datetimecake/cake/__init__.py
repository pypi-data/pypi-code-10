# -*- coding: utf-8 -*-

import functools


funcs = {}


def register(funcname=None):
    if hasattr(funcname, '__call__'):
        if funcname not in funcs:
            funcs[funcname.__name__] = funcname
        else:
            raise KeyError(
                '%s:funcname already registered' % repr(funcname))

        @functools.wraps
        def wrapper(*args, **kw):
            return funcname(*args, **kw)
        return wrapper
    else:
        def decorator(func, funcname=None):
            funcname = funcname and funcname or func.__name__
            if funcname not in funcs:
                funcs[funcname] = func
            else:
                raise KeyError(
                    '%s:funcname already registered' % repr(funcname))

            @functools.wraps
            def wrapper(*args, **kw):
                return func(*args, **kw)
            return wrapper
        ret_func = lambda func: decorator(func, funcname)
        return ret_func


class Cake(object):

    def __getattr__(self, name):
        if name in funcs:
            return funcs[name]
        else:
            raise KeyError(
                '%s:funcname Does not exist!' % repr(name))

from . import cake
