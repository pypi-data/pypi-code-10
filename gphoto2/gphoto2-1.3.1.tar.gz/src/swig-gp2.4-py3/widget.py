# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (3,0,0):
    new_instancemethod = lambda func, inst, cls: _widget.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_widget', [dirname(__file__)])
        except ImportError:
            import _widget
            return _widget
        if fp is not None:
            try:
                _mod = imp.load_module('_widget', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _widget = swig_import_helper()
    del swig_import_helper
else:
    import _widget
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


import gphoto2.camera
import gphoto2.abilities_list
import gphoto2.context
import gphoto2.list
import gphoto2.port_info_list
import gphoto2.port
import gphoto2.port_log
import gphoto2.filesys
import gphoto2.file
import gphoto2.result
class CameraWidget(object):
    """Proxy of C _CameraWidget struct"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_destroy__ = _widget.delete_CameraWidget
    def count_children(self) -> "int" :
        """
        count_children(self) -> int

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_count_children
        """
        return _widget.CameraWidget_count_children(self)

    def get_child(self, *args) -> "void" :
        """
        get_child(self, child_number)

        Parameters:
            child_number: int


        See also: gphoto2.gp_widget_get_child
        """
        return _widget.CameraWidget_get_child(self, *args)

    def get_child_by_label(self, *args) -> "void" :
        """
        get_child_by_label(self, label)

        Parameters:
            label: char const *


        See also: gphoto2.gp_widget_get_child_by_label
        """
        return _widget.CameraWidget_get_child_by_label(self, *args)

    def get_child_by_id(self, *args) -> "void" :
        """
        get_child_by_id(self, id)

        Parameters:
            id: int


        See also: gphoto2.gp_widget_get_child_by_id
        """
        return _widget.CameraWidget_get_child_by_id(self, *args)

    def get_child_by_name(self, *args) -> "void" :
        """
        get_child_by_name(self, name)

        Parameters:
            name: char const *


        See also: gphoto2.gp_widget_get_child_by_name
        """
        return _widget.CameraWidget_get_child_by_name(self, *args)

    def get_root(self) -> "void" :
        """
        get_root(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_root
        """
        return _widget.CameraWidget_get_root(self)

    def get_parent(self) -> "void" :
        """
        get_parent(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_parent
        """
        return _widget.CameraWidget_get_parent(self)

    def set_value(self, *args) -> "void" :
        """
        set_value(self, value)

        Parameters:
            value: void const *


        See also: gphoto2.gp_widget_set_value
        """
        return _widget.CameraWidget_set_value(self, *args)

    def get_value(self) -> "void" :
        """
        get_value(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_value
        """
        return _widget.CameraWidget_get_value(self)

    def set_name(self, *args) -> "void" :
        """
        set_name(self, name)

        Parameters:
            name: char const *


        See also: gphoto2.gp_widget_set_name
        """
        return _widget.CameraWidget_set_name(self, *args)

    def get_name(self) -> "void" :
        """
        get_name(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_name
        """
        return _widget.CameraWidget_get_name(self)

    def set_info(self, *args) -> "void" :
        """
        set_info(self, info)

        Parameters:
            info: char const *


        See also: gphoto2.gp_widget_set_info
        """
        return _widget.CameraWidget_set_info(self, *args)

    def get_info(self) -> "void" :
        """
        get_info(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_info
        """
        return _widget.CameraWidget_get_info(self)

    def get_id(self) -> "void" :
        """
        get_id(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_id
        """
        return _widget.CameraWidget_get_id(self)

    def get_type(self) -> "void" :
        """
        get_type(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_type
        """
        return _widget.CameraWidget_get_type(self)

    def get_label(self) -> "void" :
        """
        get_label(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_label
        """
        return _widget.CameraWidget_get_label(self)

    def set_range(self, *args) -> "void" :
        """
        set_range(self, min, max, increment)

        Parameters:
            min: float
            max: float
            increment: float


        See also: gphoto2.gp_widget_set_range
        """
        return _widget.CameraWidget_set_range(self, *args)

    def get_range(self) -> "void" :
        """
        get_range(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_range
        """
        return _widget.CameraWidget_get_range(self)

    def add_choice(self, *args) -> "void" :
        """
        add_choice(self, choice)

        Parameters:
            choice: char const *


        See also: gphoto2.gp_widget_add_choice
        """
        return _widget.CameraWidget_add_choice(self, *args)

    def count_choices(self) -> "int" :
        """
        count_choices(self) -> int

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_count_choices
        """
        return _widget.CameraWidget_count_choices(self)

    def get_choice(self, *args) -> "void" :
        """
        get_choice(self, choice_number)

        Parameters:
            choice_number: int


        See also: gphoto2.gp_widget_get_choice
        """
        return _widget.CameraWidget_get_choice(self, *args)

    def changed(self) -> "int" :
        """
        changed(self) -> int

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_changed
        """
        return _widget.CameraWidget_changed(self)

    def set_changed(self, *args) -> "void" :
        """
        set_changed(self, changed)

        Parameters:
            changed: int


        See also: gphoto2.gp_widget_set_changed
        """
        return _widget.CameraWidget_set_changed(self, *args)

    def set_readonly(self, *args) -> "void" :
        """
        set_readonly(self, readonly)

        Parameters:
            readonly: int


        See also: gphoto2.gp_widget_set_readonly
        """
        return _widget.CameraWidget_set_readonly(self, *args)

    def get_readonly(self) -> "void" :
        """
        get_readonly(self)

        Parameters:
            self: struct _CameraWidget *


        See also: gphoto2.gp_widget_get_readonly
        """
        return _widget.CameraWidget_get_readonly(self)

CameraWidget.count_children = new_instancemethod(_widget.CameraWidget_count_children,None,CameraWidget)
CameraWidget.get_child = new_instancemethod(_widget.CameraWidget_get_child,None,CameraWidget)
CameraWidget.get_child_by_label = new_instancemethod(_widget.CameraWidget_get_child_by_label,None,CameraWidget)
CameraWidget.get_child_by_id = new_instancemethod(_widget.CameraWidget_get_child_by_id,None,CameraWidget)
CameraWidget.get_child_by_name = new_instancemethod(_widget.CameraWidget_get_child_by_name,None,CameraWidget)
CameraWidget.get_root = new_instancemethod(_widget.CameraWidget_get_root,None,CameraWidget)
CameraWidget.get_parent = new_instancemethod(_widget.CameraWidget_get_parent,None,CameraWidget)
CameraWidget.set_value = new_instancemethod(_widget.CameraWidget_set_value,None,CameraWidget)
CameraWidget.get_value = new_instancemethod(_widget.CameraWidget_get_value,None,CameraWidget)
CameraWidget.set_name = new_instancemethod(_widget.CameraWidget_set_name,None,CameraWidget)
CameraWidget.get_name = new_instancemethod(_widget.CameraWidget_get_name,None,CameraWidget)
CameraWidget.set_info = new_instancemethod(_widget.CameraWidget_set_info,None,CameraWidget)
CameraWidget.get_info = new_instancemethod(_widget.CameraWidget_get_info,None,CameraWidget)
CameraWidget.get_id = new_instancemethod(_widget.CameraWidget_get_id,None,CameraWidget)
CameraWidget.get_type = new_instancemethod(_widget.CameraWidget_get_type,None,CameraWidget)
CameraWidget.get_label = new_instancemethod(_widget.CameraWidget_get_label,None,CameraWidget)
CameraWidget.set_range = new_instancemethod(_widget.CameraWidget_set_range,None,CameraWidget)
CameraWidget.get_range = new_instancemethod(_widget.CameraWidget_get_range,None,CameraWidget)
CameraWidget.add_choice = new_instancemethod(_widget.CameraWidget_add_choice,None,CameraWidget)
CameraWidget.count_choices = new_instancemethod(_widget.CameraWidget_count_choices,None,CameraWidget)
CameraWidget.get_choice = new_instancemethod(_widget.CameraWidget_get_choice,None,CameraWidget)
CameraWidget.changed = new_instancemethod(_widget.CameraWidget_changed,None,CameraWidget)
CameraWidget.set_changed = new_instancemethod(_widget.CameraWidget_set_changed,None,CameraWidget)
CameraWidget.set_readonly = new_instancemethod(_widget.CameraWidget_set_readonly,None,CameraWidget)
CameraWidget.get_readonly = new_instancemethod(_widget.CameraWidget_get_readonly,None,CameraWidget)
CameraWidget_swigregister = _widget.CameraWidget_swigregister
CameraWidget_swigregister(CameraWidget)


def gp_widget_get_value_text(*args) -> "char **" :
  """
    gp_widget_get_value_text(widget) -> int

    Parameters:
        widget: CameraWidget *

    """
  return _widget.gp_widget_get_value_text(*args)

def gp_widget_get_value_int(*args) -> "int *" :
  """
    gp_widget_get_value_int(widget) -> int

    Parameters:
        widget: CameraWidget *

    """
  return _widget.gp_widget_get_value_int(*args)

def gp_widget_get_value_float(*args) -> "float *" :
  """
    gp_widget_get_value_float(widget) -> int

    Parameters:
        widget: CameraWidget *

    """
  return _widget.gp_widget_get_value_float(*args)

def gp_widget_set_value_text(*args) -> "int" :
  """
    gp_widget_set_value_text(widget, value) -> int

    Parameters:
        widget: CameraWidget *
        value: char const *

    """
  return _widget.gp_widget_set_value_text(*args)

def gp_widget_set_value_int(*args) -> "int" :
  """
    gp_widget_set_value_int(widget, value) -> int

    Parameters:
        widget: CameraWidget *
        value: int const

    """
  return _widget.gp_widget_set_value_int(*args)

def gp_widget_set_value_float(*args) -> "int" :
  """
    gp_widget_set_value_float(widget, value) -> int

    Parameters:
        widget: CameraWidget *
        value: float const

    """
  return _widget.gp_widget_set_value_float(*args)
GP_WIDGET_WINDOW = _widget.GP_WIDGET_WINDOW
GP_WIDGET_SECTION = _widget.GP_WIDGET_SECTION
GP_WIDGET_TEXT = _widget.GP_WIDGET_TEXT
GP_WIDGET_RANGE = _widget.GP_WIDGET_RANGE
GP_WIDGET_TOGGLE = _widget.GP_WIDGET_TOGGLE
GP_WIDGET_RADIO = _widget.GP_WIDGET_RADIO
GP_WIDGET_MENU = _widget.GP_WIDGET_MENU
GP_WIDGET_BUTTON = _widget.GP_WIDGET_BUTTON
GP_WIDGET_DATE = _widget.GP_WIDGET_DATE

def gp_widget_new(*args) -> "CameraWidget **" :
  """
    gp_widget_new(type, label) -> int

    Parameters:
        type: enum CameraWidgetType
        label: char const *

    """
  return _widget.gp_widget_new(*args)

def gp_widget_append(*args) -> "int" :
  """
    gp_widget_append(widget, child) -> int

    Parameters:
        widget: CameraWidget *
        child: CameraWidget *

    """
  return _widget.gp_widget_append(*args)

def gp_widget_prepend(*args) -> "int" :
  """
    gp_widget_prepend(widget, child) -> int

    Parameters:
        widget: CameraWidget *
        child: CameraWidget *

    """
  return _widget.gp_widget_prepend(*args)

def gp_widget_count_children(*args) -> "int" :
  """
    gp_widget_count_children(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.count_children
    """
  return _widget.gp_widget_count_children(*args)

def gp_widget_get_child(*args) -> "CameraWidget **" :
  """
    gp_widget_get_child(widget, child_number) -> int

    Parameters:
        widget: CameraWidget *
        child_number: int


    See also: gphoto2.CameraWidget.get_child
    """
  return _widget.gp_widget_get_child(*args)

def gp_widget_get_child_by_label(*args) -> "CameraWidget **" :
  """
    gp_widget_get_child_by_label(widget, label) -> int

    Parameters:
        widget: CameraWidget *
        label: char const *


    See also: gphoto2.CameraWidget.get_child_by_label
    """
  return _widget.gp_widget_get_child_by_label(*args)

def gp_widget_get_child_by_id(*args) -> "CameraWidget **" :
  """
    gp_widget_get_child_by_id(widget, id) -> int

    Parameters:
        widget: CameraWidget *
        id: int


    See also: gphoto2.CameraWidget.get_child_by_id
    """
  return _widget.gp_widget_get_child_by_id(*args)

def gp_widget_get_child_by_name(*args) -> "CameraWidget **" :
  """
    gp_widget_get_child_by_name(widget, name) -> int

    Parameters:
        widget: CameraWidget *
        name: char const *


    See also: gphoto2.CameraWidget.get_child_by_name
    """
  return _widget.gp_widget_get_child_by_name(*args)

def gp_widget_get_root(*args) -> "CameraWidget **" :
  """
    gp_widget_get_root(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_root
    """
  return _widget.gp_widget_get_root(*args)

def gp_widget_get_parent(*args) -> "CameraWidget **" :
  """
    gp_widget_get_parent(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_parent
    """
  return _widget.gp_widget_get_parent(*args)

def gp_widget_set_value(*args) -> "void const *" :
  """
    gp_widget_set_value(widget, value) -> int

    Parameters:
        widget: CameraWidget *
        value: void const *


    See also: gphoto2.CameraWidget.set_value
    """
  return _widget.gp_widget_set_value(*args)

def gp_widget_get_value(*args) -> "void *" :
  """
    gp_widget_get_value(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_value
    """
  return _widget.gp_widget_get_value(*args)

def gp_widget_set_name(*args) -> "int" :
  """
    gp_widget_set_name(widget, name) -> int

    Parameters:
        widget: CameraWidget *
        name: char const *


    See also: gphoto2.CameraWidget.set_name
    """
  return _widget.gp_widget_set_name(*args)

def gp_widget_get_name(*args) -> "char **" :
  """
    gp_widget_get_name(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_name
    """
  return _widget.gp_widget_get_name(*args)

def gp_widget_set_info(*args) -> "int" :
  """
    gp_widget_set_info(widget, info) -> int

    Parameters:
        widget: CameraWidget *
        info: char const *


    See also: gphoto2.CameraWidget.set_info
    """
  return _widget.gp_widget_set_info(*args)

def gp_widget_get_info(*args) -> "char **" :
  """
    gp_widget_get_info(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_info
    """
  return _widget.gp_widget_get_info(*args)

def gp_widget_get_id(*args) -> "int *" :
  """
    gp_widget_get_id(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_id
    """
  return _widget.gp_widget_get_id(*args)

def gp_widget_get_type(*args) -> "CameraWidgetType *" :
  """
    gp_widget_get_type(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_type
    """
  return _widget.gp_widget_get_type(*args)

def gp_widget_get_label(*args) -> "char **" :
  """
    gp_widget_get_label(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_label
    """
  return _widget.gp_widget_get_label(*args)

def gp_widget_set_range(*args) -> "int" :
  """
    gp_widget_set_range(range, low, high, increment) -> int

    Parameters:
        range: CameraWidget *
        low: float
        high: float
        increment: float


    See also: gphoto2.CameraWidget.set_range
    """
  return _widget.gp_widget_set_range(*args)

def gp_widget_get_range(*args) -> "float *, float *, float *" :
  """
    gp_widget_get_range(range) -> int

    Parameters:
        range: CameraWidget *


    See also: gphoto2.CameraWidget.get_range
    """
  return _widget.gp_widget_get_range(*args)

def gp_widget_add_choice(*args) -> "int" :
  """
    gp_widget_add_choice(widget, choice) -> int

    Parameters:
        widget: CameraWidget *
        choice: char const *


    See also: gphoto2.CameraWidget.add_choice
    """
  return _widget.gp_widget_add_choice(*args)

def gp_widget_count_choices(*args) -> "int" :
  """
    gp_widget_count_choices(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.count_choices
    """
  return _widget.gp_widget_count_choices(*args)

def gp_widget_get_choice(*args) -> "char **" :
  """
    gp_widget_get_choice(widget, choice_number) -> int

    Parameters:
        widget: CameraWidget *
        choice_number: int


    See also: gphoto2.CameraWidget.get_choice
    """
  return _widget.gp_widget_get_choice(*args)

def gp_widget_changed(*args) -> "int" :
  """
    gp_widget_changed(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.changed
    """
  return _widget.gp_widget_changed(*args)

def gp_widget_set_changed(*args) -> "int" :
  """
    gp_widget_set_changed(widget, changed) -> int

    Parameters:
        widget: CameraWidget *
        changed: int


    See also: gphoto2.CameraWidget.set_changed
    """
  return _widget.gp_widget_set_changed(*args)

def gp_widget_set_readonly(*args) -> "int" :
  """
    gp_widget_set_readonly(widget, readonly) -> int

    Parameters:
        widget: CameraWidget *
        readonly: int


    See also: gphoto2.CameraWidget.set_readonly
    """
  return _widget.gp_widget_set_readonly(*args)

def gp_widget_get_readonly(*args) -> "int *" :
  """
    gp_widget_get_readonly(widget) -> int

    Parameters:
        widget: CameraWidget *


    See also: gphoto2.CameraWidget.get_readonly
    """
  return _widget.gp_widget_get_readonly(*args)


