
""" define some logistics wrapper

"""

import logging
import sys

from tingyun.packages.wrapt.wrappers import (FunctionWrapper as _FunctionWrapper)
from tingyun.packages.wrapt.wrappers import BoundFunctionWrapper as _BoundFunctionWrapper

from tingyun.packages.wrapt.wrappers import wrap_object as _wrap_object, wrap_function_wrapper as _wrap_function_wrapper
from tingyun.packages.wrapt.wrappers import function_wrapper as _function_wrapper

console = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# following method are used the wrapt module instead.
# all methods would send from this module, not use the wrapt package directly

# egg: (memcached, Client.append, MemcacheTraceWrapper(), get)
wrap_object = _wrap_object

# for wrap the function(bound/unbound)
FunctionWrapper = _FunctionWrapper
BoundFunctionWrapper = _BoundFunctionWrapper
wrap_function_wrapper = _wrap_function_wrapper
function_wrapper = _function_wrapper


def import_module(name):
    """Import module, returning the module after the last dot."""
    __import__(name)
    return sys.modules[name]


def wrap_in_function(function):
    @function_wrapper
    def _wrapper(wrapped, instance, args, kwargs):
        return function(wrapped(*args, **kwargs))
    return _wrapper


def in_function_wrapper(wrapped, function):
    return wrap_in_function(function)(wrapped)


def trace_in_function(module, object_path, function):
    return wrap_object(module, object_path, in_function_wrapper, (function, ))
