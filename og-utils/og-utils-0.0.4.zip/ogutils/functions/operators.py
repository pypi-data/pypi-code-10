from inspect import getargspec

def restrict_args(func, *args, **kwargs):
    callargs = getargspec(func)
    if not callargs.varargs:
        args = args[0:len(callargs.args)]
    return func(*args, **kwargs)

def repeat_call(func, retries, *args, **kwargs):
    '''
    Tries a total of 'retries' times to execute callable before failing.
    '''
    retries = max(0, int(retries))
    try_num = 0
    while True:
        if try_num == retries:
            return func(*args, **kwargs)
        else:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    raise e
                try_num += 1
