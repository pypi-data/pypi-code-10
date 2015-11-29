# Released under GPL3 terms (see LICENSE file)



import os
import operator
import logging

class VDict(dict):
    """Dictionary that validates keys and values"""

    def __init__(self, validators={}, valid_keys=None, *args, **kwargs):
        """
        `validators` is a dictionary that maps keys to validators. A validator
        is a callable that accept the value as a single argument and returns a
        valid value.

        `valid_keys` is an iterable of allowed keys. If unspecified, all keys
        are allowed. `KeyError` is raised if an invalid key is set.

        Any other arguments are forwarded to `update`.
        """
        super().__init__()
        self.valid_keys = valid_keys
        self.validators = validators
        self.update(**kwargs)

    def __setitem__(self, key, value):
        if self.valid_keys and key not in self.valid_keys:
            e = KeyError(key)
            e.key = key
            raise e
        else:
            if key in self.validators:
                value = self.validators[key](value)
            dict.__setitem__(self, key, value)

    def update(self, dct={}, **kwargs):
        if not isinstance(dct, dict):
            dct = dict(dct)   # Convert tuples, generator, etc to dict
        else:
            dct = dct.copy()  # Don't modify caller's dct
        if kwargs:
            dct.update(**kwargs)
        for k,v in dct.items():
            self[k] = v


_UNIT_PREFIXES = (
    ('Ki', 1024), ('Mi', 1024**2), ('Gi', 1024**3), ('Ti', 1024**4), ('Pi', 1024**5),
    ('k',  1000), ('M',  1000**2), ('G',  1000**3), ('T',  1000**4), ('P',  1000**5),
)
def str2num(val):
    """
    Convert human-readable number to integer or float

    Valid unit prefixes are k/M/G/T/P for multiples of 1000 and Ki/Mi/Gi/Ti/Pi
    for multiples of 1024. Everything after the unit prefix is ignored.

    >>> str2num('1k')
    1000.0
    >>> str2num('1 Ki')
    1024.0
    >>> str2num('4.3 Gi')
    4617089843.2

    It's also possible to calculate a fraction of a number with a percentage:

    >>> str2num('10%37')
    3.7
    >>> str2num('1%2.5')
    0.025
    >>> str2num('200%5k')
    10000
    """
    if isinstance(val, str):
        # Support infinity
        if val == 'inf':
            return float('inf')

        # 'X%Y' -> return X percent of Y
        if '%' in val:
            v1, v2 = [str2num(val) for val in val.split('%', 1)]
            return v2*v1/100

        # Find unit prefix. Everything left of it is the number; everything
        # right of it is a unit (e.g. 'B/s') and irrelevant here.
        num = val.lstrip().lower()
        for prefix,size in _UNIT_PREFIXES:
            prefix = prefix.lower()
            if prefix in num:
                prefix_pos = num.index(prefix)
                num = num[:prefix_pos].strip()
                try:
                    num = float(num) * size
                except (ValueError, TypeError):
                    raise ValueError('{!r} is not a number'.format(val))
                else:
                    break

        # Number has no known unit prefix - try extracting digits
        if not isinstance(num, (int, float)):
            try:
                num = float(''.join(c for c in num if c in '-0123456789.'))
            except ValueError:
                raise ValueError('{!r} is not a number'.format(val))

        # Float if necessary, int otherwise
        if num != float('inf'):
            num_float = float(num)
            num_int = int(num_float)
            num = num_int if num_int == num_float else num_float
    else:
        num = val

    if not isinstance(num, (int, float)):
        raise ValueError('{!r} is not a number'.format(val))
    return num


def validate_number(val, min=None, max=None, silent=False):
    """
    Validate and return float and int

    `min` and `max` set the allowed limits.

    If `silent` is True, limits are enforced silently by returning the
    min/max limit instead of the value.

    Valid unit prefixes are T/Ti, G/Gi, M/Mi and k/Ki. Case is ignored.

    Raise ValueError if validation fails.
    """
    val = str2num(val)
    # Check min/max limits
    if min is not None:
        min = str2num(min)
        if val < min:
            if silent:
                return min
            else:
                raise ValueError('{!r} is too small'.format(val))

    if max is not None:
        max = str2num(max)
        if val > max:
            if silent:
                return max
            else:
                raise ValueError('{!r} is too big'.format(val))
    return val

def validate_integer(val, min=None, max=None, silent=False):
    """
    Validate and return int only

    If `silent` is False, floats raise a ValueError, otherwise they are
    rounded.

    See `validate_number` for more documentation.
    """
    val = validate_number(val, min, max, silent)
    if not isinstance(val, int):
        if silent:
            return round(val)
        else:
            raise ValueError('{!r} is not an integer'.format(val))
    return val


TRUES = 'true 1 on yes'.split()
FALSES = 'false 0 off no'.split()
_TRUES_AND_FALSES = ', '.join(('/'.join(pair) for pair in zip(TRUES, FALSES)))
def validate_bool(val):
    """
    Validate and return boolean values case-insensitively

    True values are: true 1 on yes
    False values are: false 0 off no

    Raise ValueError if validation fails.
    """
    if str(val).lower() in TRUES:
        return True
    if str(val).lower() in FALSES:
        return False
    raise ValueError('{!r} must be one of: {}'.format(val, _TRUES_AND_FALSES))


def validate_option(val, options):
    """Return `v` if part of `options` or raise ValueError"""
    if val not in options:
        raise ValueError('{!r} must be one of: {}'.format(val, ', '.join(options)))
    return val


def validate_list(val):
    """If `val` is a list, tuple or set, return it as a list or raise ValueError"""
    if not isinstance(val, (list, tuple, set)):
        raise ValueError('{!r} must be a list'.format(val))
    return list(val)


def validate_path(path):
    """Return `path` with '~' expanded to $HOME"""
    return os.path.expanduser(path)


def validate_PATH(path):
    """
    Append `path` to the value of the environment variable `PATH` and return it

    User HOME expansion is applied with `validate_path`.
    """
    if path != '':
        path = os.pathsep.join((os.environ['PATH'], validate_path(path)))
    return path


