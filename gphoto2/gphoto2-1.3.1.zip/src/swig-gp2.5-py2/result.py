# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3,0,0):
    new_instancemethod = lambda func, inst, cls: _result.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_result', [dirname(__file__)])
        except ImportError:
            import _result
            return _result
        if fp is not None:
            try:
                _mod = imp.load_module('_result', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _result = swig_import_helper()
    del swig_import_helper
else:
    import _result
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


def _swig_setattr_nondynamic_method(set):
    def set_attr(self,name,value):
        if (name == "thisown"): return self.this.own(value)
        if hasattr(self,name) or (name == "this"):
            set(self,name,value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


GP_OK = _result.GP_OK
GP_ERROR = _result.GP_ERROR
GP_ERROR_BAD_PARAMETERS = _result.GP_ERROR_BAD_PARAMETERS
GP_ERROR_NO_MEMORY = _result.GP_ERROR_NO_MEMORY
GP_ERROR_LIBRARY = _result.GP_ERROR_LIBRARY
GP_ERROR_UNKNOWN_PORT = _result.GP_ERROR_UNKNOWN_PORT
GP_ERROR_NOT_SUPPORTED = _result.GP_ERROR_NOT_SUPPORTED
GP_ERROR_IO = _result.GP_ERROR_IO
GP_ERROR_FIXED_LIMIT_EXCEEDED = _result.GP_ERROR_FIXED_LIMIT_EXCEEDED
GP_ERROR_TIMEOUT = _result.GP_ERROR_TIMEOUT
GP_ERROR_IO_SUPPORTED_SERIAL = _result.GP_ERROR_IO_SUPPORTED_SERIAL
GP_ERROR_IO_SUPPORTED_USB = _result.GP_ERROR_IO_SUPPORTED_USB
GP_ERROR_IO_INIT = _result.GP_ERROR_IO_INIT
GP_ERROR_IO_READ = _result.GP_ERROR_IO_READ
GP_ERROR_IO_WRITE = _result.GP_ERROR_IO_WRITE
GP_ERROR_IO_UPDATE = _result.GP_ERROR_IO_UPDATE
GP_ERROR_IO_SERIAL_SPEED = _result.GP_ERROR_IO_SERIAL_SPEED
GP_ERROR_IO_USB_CLEAR_HALT = _result.GP_ERROR_IO_USB_CLEAR_HALT
GP_ERROR_IO_USB_FIND = _result.GP_ERROR_IO_USB_FIND
GP_ERROR_IO_USB_CLAIM = _result.GP_ERROR_IO_USB_CLAIM
GP_ERROR_IO_LOCK = _result.GP_ERROR_IO_LOCK
GP_ERROR_HAL = _result.GP_ERROR_HAL

def gp_port_result_as_string(*args):
  """
    gp_port_result_as_string(result) -> char const *

    Parameters:
        result: int

    """
  return _result.gp_port_result_as_string(*args)
GP_ERROR_CORRUPTED_DATA = _result.GP_ERROR_CORRUPTED_DATA
GP_ERROR_FILE_EXISTS = _result.GP_ERROR_FILE_EXISTS
GP_ERROR_MODEL_NOT_FOUND = _result.GP_ERROR_MODEL_NOT_FOUND
GP_ERROR_DIRECTORY_NOT_FOUND = _result.GP_ERROR_DIRECTORY_NOT_FOUND
GP_ERROR_FILE_NOT_FOUND = _result.GP_ERROR_FILE_NOT_FOUND
GP_ERROR_DIRECTORY_EXISTS = _result.GP_ERROR_DIRECTORY_EXISTS
GP_ERROR_CAMERA_BUSY = _result.GP_ERROR_CAMERA_BUSY
GP_ERROR_PATH_NOT_ABSOLUTE = _result.GP_ERROR_PATH_NOT_ABSOLUTE
GP_ERROR_CANCEL = _result.GP_ERROR_CANCEL
GP_ERROR_CAMERA_ERROR = _result.GP_ERROR_CAMERA_ERROR
GP_ERROR_OS_FAILURE = _result.GP_ERROR_OS_FAILURE
GP_ERROR_NO_SPACE = _result.GP_ERROR_NO_SPACE

def gp_result_as_string(*args):
  """
    gp_result_as_string(result) -> char const *

    Parameters:
        result: int

    """
  return _result.gp_result_as_string(*args)
import logging

class GPhoto2Error(Exception):
    """Exception raised by gphoto2 library errors

    Attributes:
        code   (int): the gphoto2 error code
        string (str): corresponding error message
    """
    def __init__(self, code):
        string = gp_result_as_string(code)
        Exception.__init__(self, '[%d] %s' % (code, string))
        self.code = code
        self.string = string

# 'hide' true location of this definition
GPhoto2Error.__module__ = 'gphoto2'

# user adjustable check_result lookup table
error_severity = {
    GP_ERROR_CANCEL           : logging.INFO,
    GP_ERROR_DIRECTORY_EXISTS : logging.WARNING,
    }
error_exception = logging.ERROR

_return_logger = logging.getLogger('gphoto2.returnvalue')

def check_result(result):
    """Pops gphoto2 'error' value from 'result' list and checks it.

    If there is no error the remaining result is returned. For other
    errors a severity level is taken from the error_severity dict, or
    set to logging.CRITICAL if the error is not in error_severity.

    If the severity >= error_exception an exception is raised.
    Otherwise a message is logged at the appropriate severity level.
    """

    if not isinstance(result, (tuple, list)):
        error = result
    elif len(result) == 2:
        error, result = result
    else:
        error = result[0]
        result = result[1:]
    if error >= GP_OK:
        return result
    severity = logging.CRITICAL
    if error in error_severity:
        severity = error_severity[error]
    if severity >= error_exception:
        raise GPhoto2Error(error)
    _return_logger.log(severity, '[%d] %s', error, gp_result_as_string(error))
    return result



