# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3,0,0):
    new_instancemethod = lambda func, inst, cls: _list.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_list', [dirname(__file__)])
        except ImportError:
            import _list
            return _list
        if fp is not None:
            try:
                _mod = imp.load_module('_list', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _list = swig_import_helper()
    del swig_import_helper
else:
    import _list
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


class CameraList(object):
    """Proxy of C _CameraList struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        """__init__(self) -> CameraList"""
        _list.CameraList_swiginit(self,_list.new_CameraList())
    __swig_destroy__ = _list.delete_CameraList
    def __len__(self) -> "int" :
        """
        __len__(self) -> int

        Parameters:
            self: struct _CameraList *


        See also: gphoto2.gp_list_count
        """
        return _list.CameraList___len__(self)

    def __getitem__(self, *args) -> "PyObject *" :
        """
        __getitem__(self, idx) -> PyObject *

        Parameters:
            idx: int


        See also: gphoto2.gp_list_count
        """
        return _list.CameraList___getitem__(self, *args)

    def count(self) -> "int" :
        """
        count(self) -> int

        Parameters:
            self: struct _CameraList *


        See also: gphoto2.gp_list_count
        """
        return _list.CameraList_count(self)

    def append(self, *args) -> "void" :
        """
        append(self, name, value)

        Parameters:
            name: char const *
            value: char const *


        See also: gphoto2.gp_list_append
        """
        return _list.CameraList_append(self, *args)

    def reset(self) -> "void" :
        """
        reset(self)

        Parameters:
            self: struct _CameraList *


        See also: gphoto2.gp_list_reset
        """
        return _list.CameraList_reset(self)

    def sort(self) -> "void" :
        """
        sort(self)

        Parameters:
            self: struct _CameraList *


        See also: gphoto2.gp_list_sort
        """
        return _list.CameraList_sort(self)

    def find_by_name(self, *args) -> "void" :
        """
        find_by_name(self, index, name)

        Parameters:
            index: int *
            name: char const *


        See also: gphoto2.gp_list_find_by_name
        """
        return _list.CameraList_find_by_name(self, *args)

    def get_name(self, *args) -> "void" :
        """
        get_name(self, index)

        Parameters:
            index: int


        See also: gphoto2.gp_list_get_name
        """
        return _list.CameraList_get_name(self, *args)

    def get_value(self, *args) -> "void" :
        """
        get_value(self, index)

        Parameters:
            index: int


        See also: gphoto2.gp_list_get_value
        """
        return _list.CameraList_get_value(self, *args)

    def set_name(self, *args) -> "void" :
        """
        set_name(self, index, name)

        Parameters:
            index: int
            name: char const *


        See also: gphoto2.gp_list_set_name
        """
        return _list.CameraList_set_name(self, *args)

    def set_value(self, *args) -> "void" :
        """
        set_value(self, index, value)

        Parameters:
            index: int
            value: char const *


        See also: gphoto2.gp_list_set_value
        """
        return _list.CameraList_set_value(self, *args)

    def populate(self, *args) -> "void" :
        """
        populate(self, format, count)

        Parameters:
            format: char const *
            count: int


        See also: gphoto2.gp_list_populate
        """
        return _list.CameraList_populate(self, *args)

CameraList.__len__ = new_instancemethod(_list.CameraList___len__,None,CameraList)
CameraList.__getitem__ = new_instancemethod(_list.CameraList___getitem__,None,CameraList)
CameraList.count = new_instancemethod(_list.CameraList_count,None,CameraList)
CameraList.append = new_instancemethod(_list.CameraList_append,None,CameraList)
CameraList.reset = new_instancemethod(_list.CameraList_reset,None,CameraList)
CameraList.sort = new_instancemethod(_list.CameraList_sort,None,CameraList)
CameraList.find_by_name = new_instancemethod(_list.CameraList_find_by_name,None,CameraList)
CameraList.get_name = new_instancemethod(_list.CameraList_get_name,None,CameraList)
CameraList.get_value = new_instancemethod(_list.CameraList_get_value,None,CameraList)
CameraList.set_name = new_instancemethod(_list.CameraList_set_name,None,CameraList)
CameraList.set_value = new_instancemethod(_list.CameraList_set_value,None,CameraList)
CameraList.populate = new_instancemethod(_list.CameraList_populate,None,CameraList)
CameraList_swigregister = _list.CameraList_swigregister
CameraList_swigregister(CameraList)


def gp_list_new() -> "CameraList **" :
  """gp_list_new() -> int"""
  return _list.gp_list_new()

def gp_list_count(*args) -> "int" :
  """
    gp_list_count(list) -> int

    Parameters:
        list: CameraList *


    See also: gphoto2.CameraList.count
    """
  return _list.gp_list_count(*args)

def gp_list_append(*args) -> "int" :
  """
    gp_list_append(list, name, value) -> int

    Parameters:
        list: CameraList *
        name: char const *
        value: char const *


    See also: gphoto2.CameraList.append
    """
  return _list.gp_list_append(*args)

def gp_list_reset(*args) -> "int" :
  """
    gp_list_reset(list) -> int

    Parameters:
        list: CameraList *


    See also: gphoto2.CameraList.reset
    """
  return _list.gp_list_reset(*args)

def gp_list_sort(*args) -> "int" :
  """
    gp_list_sort(list) -> int

    Parameters:
        list: CameraList *


    See also: gphoto2.CameraList.sort
    """
  return _list.gp_list_sort(*args)

def gp_list_find_by_name(*args) -> "int" :
  """
    gp_list_find_by_name(list, index, name) -> int

    Parameters:
        list: CameraList *
        index: int *
        name: char const *


    See also: gphoto2.CameraList.find_by_name
    """
  return _list.gp_list_find_by_name(*args)

def gp_list_get_name(*args) -> "char **" :
  """
    gp_list_get_name(list, index) -> int

    Parameters:
        list: CameraList *
        index: int


    See also: gphoto2.CameraList.get_name
    """
  return _list.gp_list_get_name(*args)

def gp_list_get_value(*args) -> "char **" :
  """
    gp_list_get_value(list, index) -> int

    Parameters:
        list: CameraList *
        index: int


    See also: gphoto2.CameraList.get_value
    """
  return _list.gp_list_get_value(*args)

def gp_list_set_name(*args) -> "int" :
  """
    gp_list_set_name(list, index, name) -> int

    Parameters:
        list: CameraList *
        index: int
        name: char const *


    See also: gphoto2.CameraList.set_name
    """
  return _list.gp_list_set_name(*args)

def gp_list_set_value(*args) -> "int" :
  """
    gp_list_set_value(list, index, value) -> int

    Parameters:
        list: CameraList *
        index: int
        value: char const *


    See also: gphoto2.CameraList.set_value
    """
  return _list.gp_list_set_value(*args)

def gp_list_populate(*args) -> "int" :
  """
    gp_list_populate(list, format, count) -> int

    Parameters:
        list: CameraList *
        format: char const *
        count: int


    See also: gphoto2.CameraList.populate
    """
  return _list.gp_list_populate(*args)


