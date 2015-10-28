"""
Ginga is a toolkit designed for building viewers for scientific image
data in Python, visualizing 2D pixel data in numpy arrays.
The Ginga toolkit centers around an image display class which supports
zooming and panning, color and intensity mapping, a choice of several
automatic cut levels algorithms and canvases for plotting scalable
geometric forms.  In addition to this widget, a general purpose
'reference' FITS viewer is provided, based on a plugin framework.

Copyright (c) 2011-2015 Eric R. Jeschke. All rights reserved.

Ginga is distributed under an open-source BSD licence. Please see the
file LICENSE.txt in the top-level directory for details.
"""

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''

try:
    # As long as we're using setuptools/distribute, we need to do this the
    # setuptools way or else pkg_resources will throw up unncessary and
    # annoying warnings (even though the namespace mechanism will still
    # otherwise work without it).
    # Get rid of this as soon as setuptools/distribute is dead.
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

#END
