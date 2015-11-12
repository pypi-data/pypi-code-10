def is_collection(elem):
    return hasattr(elem, '__iter__') or hasattr(elem, '__getitem__')

def is_empty(elem):
    return is_collection(elem) and not any(True for _ in elem)

def any_shared(enum_one, enum_two):
    if not is_collection(enum_one) or not is_collection(enum_two):
        return False
    enum_one = enum_one if isinstance(enum_one, (set, dict)) else set(enum_one)
    enum_two = enum_two if isinstance(enum_two, (set, dict)) else set(enum_two)
    return any(e in enum_two for e in enum_one)
