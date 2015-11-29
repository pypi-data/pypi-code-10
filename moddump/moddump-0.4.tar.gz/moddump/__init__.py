import glob

__version__ = '0.4'
__locales__ = glob.glob('moddump/locales/*.json')

from . import dump
from . import heroes