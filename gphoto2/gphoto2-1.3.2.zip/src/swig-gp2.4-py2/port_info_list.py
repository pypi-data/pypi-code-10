# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3,0,0):
    new_instancemethod = lambda func, inst, cls: _port_info_list.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_port_info_list', [dirname(__file__)])
        except ImportError:
            import _port_info_list
            return _port_info_list
        if fp is not None:
            try:
                _mod = imp.load_module('_port_info_list', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _port_info_list = swig_import_helper()
    del swig_import_helper
else:
    import _port_info_list
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


import gphoto2.port
class PortInfoList(object):
    """Proxy of C _GPPortInfoList struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        """__init__(self) -> PortInfoList"""
        _port_info_list.PortInfoList_swiginit(self,_port_info_list.new_PortInfoList())
    __swig_destroy__ = _port_info_list.delete_PortInfoList
    def __len__(self):
        """
        __len__(self) -> int

        Parameters:
            self: struct _GPPortInfoList *


        See also: gphoto2.gp_port_info_list_count
        """
        return _port_info_list.PortInfoList___len__(self)

    def __getitem__(self, *args):
        """
        __getitem__(self, idx)

        Parameters:
            idx: int


        See also: gphoto2.gp_port_info_list_count
        """
        return _port_info_list.PortInfoList___getitem__(self, *args)

    def append(self, *args):
        """
        append(self, info)

        Parameters:
            info: GPPortInfo


        See also: gphoto2.gp_port_info_list_append
        """
        return _port_info_list.PortInfoList_append(self, *args)

    def load(self):
        """
        load(self)

        Parameters:
            self: struct _GPPortInfoList *


        See also: gphoto2.gp_port_info_list_load
        """
        return _port_info_list.PortInfoList_load(self)

    def count(self):
        """
        count(self) -> int

        Parameters:
            self: struct _GPPortInfoList *


        See also: gphoto2.gp_port_info_list_count
        """
        return _port_info_list.PortInfoList_count(self)

    def lookup_path(self, *args):
        """
        lookup_path(self, path) -> int

        Parameters:
            path: char const *


        See also: gphoto2.gp_port_info_list_lookup_path
        """
        return _port_info_list.PortInfoList_lookup_path(self, *args)

    def lookup_name(self, *args):
        """
        lookup_name(self, name) -> int

        Parameters:
            name: char const *


        See also: gphoto2.gp_port_info_list_lookup_name
        """
        return _port_info_list.PortInfoList_lookup_name(self, *args)

    def get_info(self, *args):
        """
        get_info(self, n)

        Parameters:
            n: int const


        See also: gphoto2.gp_port_info_list_get_info
        """
        return _port_info_list.PortInfoList_get_info(self, *args)

PortInfoList.__len__ = new_instancemethod(_port_info_list.PortInfoList___len__,None,PortInfoList)
PortInfoList.__getitem__ = new_instancemethod(_port_info_list.PortInfoList___getitem__,None,PortInfoList)
PortInfoList.append = new_instancemethod(_port_info_list.PortInfoList_append,None,PortInfoList)
PortInfoList.load = new_instancemethod(_port_info_list.PortInfoList_load,None,PortInfoList)
PortInfoList.count = new_instancemethod(_port_info_list.PortInfoList_count,None,PortInfoList)
PortInfoList.lookup_path = new_instancemethod(_port_info_list.PortInfoList_lookup_path,None,PortInfoList)
PortInfoList.lookup_name = new_instancemethod(_port_info_list.PortInfoList_lookup_name,None,PortInfoList)
PortInfoList.get_info = new_instancemethod(_port_info_list.PortInfoList_get_info,None,PortInfoList)
PortInfoList_swigregister = _port_info_list.PortInfoList_swigregister
PortInfoList_swigregister(PortInfoList)

GP_PORT_NONE = _port_info_list.GP_PORT_NONE
GP_PORT_SERIAL = _port_info_list.GP_PORT_SERIAL
GP_PORT_USB = _port_info_list.GP_PORT_USB
GP_PORT_DISK = _port_info_list.GP_PORT_DISK
GP_PORT_PTPIP = _port_info_list.GP_PORT_PTPIP
GP_PORT_USB_DISK_DIRECT = _port_info_list.GP_PORT_USB_DISK_DIRECT
GP_PORT_USB_SCSI = _port_info_list.GP_PORT_USB_SCSI
class GPPortInfo(object):
    """Proxy of C _GPPortInfo struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    type = _swig_property(_port_info_list.GPPortInfo_type_get, _port_info_list.GPPortInfo_type_set)
    name = _swig_property(_port_info_list.GPPortInfo_name_get, _port_info_list.GPPortInfo_name_set)
    path = _swig_property(_port_info_list.GPPortInfo_path_get, _port_info_list.GPPortInfo_path_set)
    library_filename = _swig_property(_port_info_list.GPPortInfo_library_filename_get, _port_info_list.GPPortInfo_library_filename_set)
    __swig_destroy__ = _port_info_list.delete_GPPortInfo
GPPortInfo_swigregister = _port_info_list.GPPortInfo_swigregister
GPPortInfo_swigregister(GPPortInfo)


def gp_port_info_list_new():
  """gp_port_info_list_new() -> int"""
  return _port_info_list.gp_port_info_list_new()

def gp_port_info_list_append(*args):
  """
    gp_port_info_list_append(list, info) -> int

    Parameters:
        list: PortInfoList *
        info: GPPortInfo


    See also: gphoto2.PortInfoList.append
    """
  return _port_info_list.gp_port_info_list_append(*args)

def gp_port_info_list_load(*args):
  """
    gp_port_info_list_load(list) -> int

    Parameters:
        list: PortInfoList *


    See also: gphoto2.PortInfoList.load
    """
  return _port_info_list.gp_port_info_list_load(*args)

def gp_port_info_list_count(*args):
  """
    gp_port_info_list_count(list) -> int

    Parameters:
        list: PortInfoList *


    See also: gphoto2.PortInfoList.count
    """
  return _port_info_list.gp_port_info_list_count(*args)

def gp_port_info_list_lookup_path(*args):
  """
    gp_port_info_list_lookup_path(list, path) -> int

    Parameters:
        list: PortInfoList *
        path: char const *


    See also: gphoto2.PortInfoList.lookup_path
    """
  return _port_info_list.gp_port_info_list_lookup_path(*args)

def gp_port_info_list_lookup_name(*args):
  """
    gp_port_info_list_lookup_name(list, name) -> int

    Parameters:
        list: PortInfoList *
        name: char const *


    See also: gphoto2.PortInfoList.lookup_name
    """
  return _port_info_list.gp_port_info_list_lookup_name(*args)

def gp_port_info_list_get_info(*args):
  """
    gp_port_info_list_get_info(list, n) -> int

    Parameters:
        list: PortInfoList *
        n: int


    See also: gphoto2.PortInfoList.get_info
    """
  return _port_info_list.gp_port_info_list_get_info(*args)

def gp_port_message_codeset(*args):
  """
    gp_port_message_codeset(arg1) -> char const *

    Parameters:
        arg1: char const *

    """
  return _port_info_list.gp_port_message_codeset(*args)


