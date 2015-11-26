# import Libraries of other lib packages
import bob.io.base

from ._library import *
from . import version
from .version import module as __version__

def get_config():
  """Returns a string containing the configuration information.
  """

  import bob.extension
  return bob.extension.get_config(__name__, version.externals)


# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]

# Setup default model for C-API
from pkg_resources import resource_filename
import os.path
from ._library import __set_default_model__
__set_default_model__(resource_filename(__name__, os.path.join('data', 'flandmark_model.dat')))
del resource_filename, __set_default_model__, os
