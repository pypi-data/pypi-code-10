from ..functions.operators import restrict_args

def apply_dict_default(dictionary, arg, default):
    '''
    Used to avoid generating a defaultdict object, or assigning defaults to a dict-like object
    '''
    if arg not in dictionary:
        if hasattr(default, '__call__'):
            # Don't try/catch because the method could raise a TypeError and we'd hide it
            default = restrict_args(default, arg)
        dictionary[arg] = default
    return dictionary
