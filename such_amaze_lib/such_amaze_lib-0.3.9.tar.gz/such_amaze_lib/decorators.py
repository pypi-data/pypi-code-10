"""
    contain useful decorators
"""
import time


def wrapper_printer(before='Before', after='After'):
    """
        Decorator that print before and after the function execution
    :param before: printed before the execution of the function
    :param after: printed after the execution of the function

        :Example:

            >>> @wrapper_printer('hello', 'goodbye')
            ... def foo():
            ...     print 'bar'
            ... 
            >>> foo()
            hello
            bar
            goodbye
    """

    def func_wrapper(func):
        def wrapper(*args, **kwargs):
            print before
            fun_return = func(*args, **kwargs)
            print after
            return fun_return

        return wrapper

    return func_wrapper


def wrapper_timer(func):
    """
        Print on console the time a function spend executing

        :Example:

            >>> import time
            >>> @wrapper_timer
            ... def foo():
            ...     time.sleep(.42)
            ...     return 'bar'
            >>> foo()
            foo executed in ...s
            'bar'
    """

    def wrapper(*args, **kwargs):
        t = time.time()
        fun_return = func(*args, **kwargs)
        d = time.time() - t
        print '{} executed in {}s'.format(func.__name__, round(d, 2))
        return fun_return

    return wrapper


def wrapper_cache(func):
    """
        Create a cache that memorize the results each function call

        :Example:

            >>> @wrapper_cache
            ... def wait(t):
            ...     print 'waiting {}s...'.format(t)
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
