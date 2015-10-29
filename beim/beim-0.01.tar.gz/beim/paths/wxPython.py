"""
handle paths for wxPython
"""

name = 'wxPython'
description = 'wx python'

from .InstallationNotFound import InstallationNotFound

try:
    import wx
except ImportError:
    raise InstallationNotFound("wx python")


import os

def find():
    from .Paths import Paths
    paths = Paths( name, description = description )
    return paths
