# -*- coding: utf-8 -*-

from functools import wraps
import inspect
import types
import uuid
import math

def tolerant_equals(a, b, atol=10e-7, rtol=10e-7):
    return math.fabs(a - b) <= (atol + rtol * math.fabs(b))

def isint(num):
    return isinstance(num, (int, long))

def isnumber(num):
    return isinstance(num, (int, long, float))

def get_caller_name(skip=2):
    """Get a name of a caller in the format module.class.method
    
       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
       
       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]   
    
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method
    del parentframe
    return name

def generate_uuid():
    return uuid.uuid4().hex