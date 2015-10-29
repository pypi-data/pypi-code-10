"""
handle paths for mmtk
"""

name = 'mmtk'
description = 'mmtk'


from .InstallationNotFound import InstallationNotFound

try:
    from . import MMTK
except ImportError as err:
    import traceback
    print(traceback.format_exc())
    raise InstallationNotFound(name)

import os


def find():
    from .Paths import Paths
    paths = Paths(name, description = description)
    return paths
