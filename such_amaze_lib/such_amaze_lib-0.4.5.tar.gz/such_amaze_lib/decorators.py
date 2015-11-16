"""
    contain useful decorators
"""
from __future__ import print_function
import time


def wrapper_printer(before='Before', after='After', end='\n'):
    """
        Decorator that print before and after the function execution
    :param before: printed before the execution of the function
    :param after: printed after the execution of the function
    :param end: end of line string

        :Example:

            >>> @wrapper_printer('hello', 'goodbye')
            ... def foo():
            ...     print('bar')
            ... 
            >>> foo()
            hello
            bar
            goodbye
    """

    def wrapper_factory(func):
        def wrapper(*args, **kwargs):
            print(before, end=end)
            fun_return = func(*args, **kwargs)
            print(after, end=end)
            return fun_return

        return wrapper

    return wrapper_factory


def wrapper_timer(round_num=2):
    """
        Print on console the time a function spend executing

        :Example:

            >>> import time
            >>> @wrapper_timer()
            ... def foo():
            ...     time.sleep(.42)
            ...     return 'bar'
            >>> foo()
            foo executed in ...s
            'bar'
    """

    def wrapper_factory(func):
        def wrapper(*args, **kwargs):
            t = time.time()
            fun_return = func(*args, **kwargs)
            d = time.time() - t
            print('{} executed in {}s'.format(func.__name__, round(d, round_num)))
            return fun_return

        return wrapper

    return wrapper_factory


def wrapper_cache(func):
    """
        Create a cache that memorize the results each function call

        :Example:

            >>> @wrapper_cache
            ... def wait(t):
            ...     print('waiting {}s...'.format(t))
            ...     import time
            ...     time.sleep(t)
            ...     return t
            ... 
            >>> wait(1)
            waiting 1s...
            1
            >>> wait(1)
            1

    """
    _cache = dict()

    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if not _cache.get(key):
            _cache[key] = func(*args, **kwargs)
        return _cache[key]

    return wrapper
