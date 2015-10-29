"""
handle paths for matplotlib
"""

name = 'matplotlib'
description = 'python plotting package'

from .InstallationNotFound import InstallationNotFound

try:
    import pylab
except ImportError:
    raise InstallationNotFound("matplotlib")


import os

def find():
    from .Paths import Paths
    paths = Paths( name, description = description )

    return paths
