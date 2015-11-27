# -*- coding: utf-8 -*-

import argparse
import os

from . import paths

_loaded = {}


def load(path):
    """..."""
    path = os.path.abspath(paths.interpret([path])[0])
    if not os.path.isfile(path):
        path = os.path.join(path, 'cook.py')

    if path in _loaded:
        if _loaded[path] is False:
            raise ImportError('Cyclic import of {}'.format(path))
        return _loaded[path]

    # Mark this as being currently loaded.
    _loaded[path] = False

    variables = {}
    with open(path) as f:
        exec(compile(f.read(), path, 'exec'), {}, variables)

    namespace = argparse.Namespace()
    for name, value in variables.items():
        setattr(namespace, name, value)

    _loaded[path] = namespace

    return namespace
