"""
handle paths for h5py
"""

name = 'py_h5py'
description = 'numerical python'


from .InstallationNotFound import InstallationNotFound

try:
    import h5py
except ImportError as err:
    import traceback
    tb = traceback.format_exc()
    raise InstallationNotFound(
        errormessage = tb,
        packagename = 'h5py',
        possible_solution = "Install h5py and make sure its path is in python import path",
        )

import os


def find():
    from .Paths import Paths
    paths = Paths( name, description = description)
    return paths
