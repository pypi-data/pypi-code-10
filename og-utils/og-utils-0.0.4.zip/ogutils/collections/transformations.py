from checks import is_collection

def recursive_iter(enumerables):
    if not is_collection(enumerables) or isinstance(enumerables, basestring):
        yield enumerables
    else:
        for elem in enumerables:
            for sub_elem in recursive_iter(elem):
                yield sub_elem

def flatten(enumerable):
    return list(recursive_iter(enumerable))
