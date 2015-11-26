"""
XStatic resource package

See package 'XStatic' for documentation and basic tools.
"""

DISPLAY_NAME = 'Chart.js' # official name, upper/lowercase allowed, no spaces
PACKAGE_NAME = 'XStatic-%s' % DISPLAY_NAME # name used for PyPi

NAME = __name__.split('.')[-1] # package name (e.g. 'foo' or 'foo_bar')
                               # please use a all-lowercase valid python
                               # package name

VERSION = '1.0.2' # version of the packaged files, please use the upstream
                   # version number
BUILD = '2'  # our package build number, so we can release new builds
             # with fixes for xstatic stuff.
PACKAGE_VERSION = VERSION + '.' + BUILD # version used for PyPi

DESCRIPTION = "%s %s (XStatic packaging standard)" % (DISPLAY_NAME, VERSION)

PLATFORMS = 'any'
CLASSIFIERS = []
KEYWORDS = '%s xstatic' % NAME

# XStatic-* package maintainer:
MAINTAINER = 'Benjamin Dauvergne'
MAINTAINER_EMAIL = 'bdauvergne@entrouvert.com'

# this refers to the project homepage of the stuff we packaged:
HOMEPAGE = 'https://github.com/nnnick/Chart.js'

# this refers to all files:
LICENSE = '(same as %s)' % DISPLAY_NAME

from os.path import join, dirname
BASE_DIR = join(dirname(__file__), 'data')

LOCATIONS = {}
