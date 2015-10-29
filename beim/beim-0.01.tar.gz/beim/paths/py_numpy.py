"""
handle paths for numpy
"""

name = 'py_numpy'
description = 'numerical python'


from .InstallationNotFound import InstallationNotFound

try:
    import numpy
except ImportError as err:
    import traceback
    print(traceback.format_exc())
    raise InstallationNotFound(name)

import os
# numpy is strange because it installs its headers to python directory
include = os.path.join( os.path.split( numpy.__file__ )[0],
                        "core", "include" )

def find():
    from .Paths import Paths
    paths = Paths( name, description = description, includes = [include] )
    return paths
