# -*- coding: utf-8 -*-

import os
import inspect
import sys

# The currently executed script always has a relative __file__ path.
# When changing the current working directory, this path becomes invalid.
# This is a workaround which should be replaced soon.
_old_main = None
_replacement = None


def find_script(ignore=1):
    """Find the path to the first cook.py-file of the call stack.

    Ignore specifies the number of frames which should be ignored.
    """
    depth = ignore + 1
    while True:
        path = inspect.getfile(sys._getframe(depth))
        if path == _old_main:
            path = _replacement
        if path.endswith('cook.py'):
            return path
        depth += 1


def _interpret(paths):
    """Interpret all paths relative to the current cook.py-script."""
    directory = os.path.dirname(find_script(ignore=2))

    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        if path[0] == ':':
            yield path[1:]
        elif os.path.isabs(path):
            yield path
        else:
            yield os.path.normpath(os.path.join(directory, path))


def interpret(paths):
    return list(_interpret(paths))
