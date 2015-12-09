# Django <1.9 provides importlib for Python <2.6
try:
    from importlib import import_module  # noqa
except ImportError:
    from django.utils.importlib import import_module  # noqa

# Django <1.9 provides SortedDict on older versions for Python < 2.6
try:
    from collections import OrderedDict  # noqa
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict  # noqa

# Django <1.6 provides update_wrapper for Python < 2.6
try:
    from functools import update_wrapper  # noqa
except ImportError:
    from django.utils.functional import update_wrapper  # noqa

# Checks framework only exists on Django 1.7+
try:
    from django.core.checks import Error, Tags, register
except ImportError:
    class CheckMessage(object):
        def __init__(self, level, msg, hint=None, obj=None, id=None):
            self.level = level
            self.msg = msg
            self.hint = hint
            self.obj = obj
            self.id = id

    class Error(CheckMessage):
        def __init__(self, *args, **kwargs):
            super(Error, self).__init__(40, *args, **kwargs)

    Tags = object()

    def register():
        pass
