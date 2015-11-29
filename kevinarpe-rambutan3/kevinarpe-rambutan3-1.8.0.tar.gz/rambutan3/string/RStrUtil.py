from rambutan3 import RArgs


def auto_quote(value) -> str:
    if isinstance(value, str):
        # Adds leading and trailing quotes, e.g., 'abc', "a'b'c", 'a"b"c'
        x = repr(value)
    else:
        x = str(value)

    return x


def __auto_quote_iterable(iterable, *, prefix: str, suffix: str):
    y = ', '.join([auto_quote(x) for x in iterable])
    z = prefix + y + suffix
    return z


def auto_quote_tuple(tuple_: tuple) -> str:
    RArgs.check_is_instance(tuple_, tuple, 'tuple_')

    x = __auto_quote_iterable(tuple_, prefix='(', suffix=')')
    return x


def auto_quote_list(list_: list) -> str:
    RArgs.check_is_instance(list_, list, 'list_')

    x = __auto_quote_iterable(list_, prefix='[', suffix=']')
    return x


def auto_quote_set(set_: set) -> str:
    RArgs.check_is_instance(set_, set, 'set_')

    # Special exception for sets: There is no built-in syntax for an empty set.
    # {} denotes an empty dict.
    if 0 == len(set_):
        return 'set()'

    x = __auto_quote_iterable(set_, prefix='{', suffix='}')
    return x


def auto_quote_dict(dict_: dict) -> str:
    RArgs.check_is_instance(dict_, dict, 'dict_')

    x = \
        '{' \
        + ', '.join(
            [
                auto_quote(key) + ': ' + auto_quote(value)
                for key, value in dict_.items()
            ]) \
        + '}'
    return x
