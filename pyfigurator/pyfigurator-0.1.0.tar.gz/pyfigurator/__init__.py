from .config import Config
from .error import *

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
