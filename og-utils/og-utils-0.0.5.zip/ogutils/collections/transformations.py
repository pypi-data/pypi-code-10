from checks import is_collection

def recursive_iter(enumerables):
    if not is_collection(enumerables) or isinstance(enumerables, (basestring, dict)):
        yield enumerables
    else:
        for elem in enumerables:
            for sub_elem in recursive_iter(elem):
                yield sub_elem

def flatten(enumerable):
    return list(recursive_iter(enumerable))

def merge_dicts(*dicts, **copy_check):
    '''
    Combines dictionaries into a single dictionary. If the 'copy' keyword is passed
    then the first dictionary is copied before update.

    merge_dicts({'a': 1, 'c': 1}, {'a': 2, 'b': 1})
    # => {'a': 2, 'b': 1, 'c': 1}
    '''
    merged = {}
    if not dicts:
        return merged
    for index, merge_dict in enumerate(dicts):
        if index == 0 and not copy_check.get('copy'):
            merged = merge_dict
        else:
            merged.update(merge_dict)
    return merged
