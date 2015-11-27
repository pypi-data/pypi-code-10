# -*- coding: utf-8 -*-

"""A cross-platform, free and open-source build system."""

from . import platform
from .arguments import argument
from .ninja import build
from .other import load
from .paths import interpret
from .rules import cpp_executable, cpp_library, configure
from .types import Namespace

# We only want to have side-effects cookpy is imported like
# >>> from cookpy import *
# This may be a bit of a hack and should be improved!
import inspect
try:
    code = inspect.stack()[-1][4][0]
except TypeError:
    pass
else:
    if '*' in code:
        from . import setup
        setup.init()
        del setup
    del code
del inspect

__version__ = '0.0.0'
