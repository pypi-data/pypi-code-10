__author__ = 'benjamin.c.yan'

import json

from .dynamic_class import make_dynamic_class


_knapsack = {}

_random_seed = 0


def object2dict(obj):
    d = {}
    for key in obj:
        d[key] = obj[key]
    return d


def object_hook(obj):
    unique_id = _unique(obj)
    if unique_id in _knapsack:
        dynamic_class = _knapsack[unique_id]
    else:
        dynamic_class = make_dynamic_class(_random_name(), obj.keys())
        _knapsack[unique_id] = dynamic_class

    obj = dynamic_class(obj)
    return obj


def _random_name():
    global _random_seed
    _random_seed += 1
    return 'Dolphin_%d' % _random_seed


def _unique(obj):
    tmp = tuple([(key, type(obj[key])) for key in sorted(obj.keys())])
    return hash(tmp)


def dumps(obj, *args, **kwargs):
    if hasattr(obj, "__identifier__") and obj.__identifier__ == "dolphin":
        kwargs['default'] = object2dict

    return json.dumps(obj, *args, **kwargs)


def dump(obj, fp, *args, **kwargs):
    if hasattr(obj, "__identifier__") and obj.__identifier__ == "dolphin":
        kwargs['default'] = object2dict

    json.dump(obj, fp, *args, **kwargs)


def _load(fn):
    def tmp(src, *args, **kwargs):
        try:
            kwargs['object_hook'] = object_hook
            return fn(src, *args, **kwargs)
        except ValueError:
            return None

    return tmp


load = _load(json.load)
loads = _load(json.loads)

