# Author: Joel Frederico
"""
This project is designed to make version checking easier in scripts. A common development problem of scripts is that they depend on older versions of packages that have evolved.  These scripts may have incompatibilities with the newer modules that result in the scripts breaking. It is then very difficult to track down which version of the module the script depends on if it was never recorded which version of the module the script is built against.
"""
__version__ = '1.2.0'

__all__ = [
    'CheckMod',
    'vcheck'
    ]
__all__.sort()

from .checkmod import CheckMod
from .vcheck import *
from .versionerror import VersionError
