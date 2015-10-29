#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def get( package, type = 'src', version = None, platform = None, pyver = None,
         **kwds ):
    modulename = "%s.%s" % (package, type)
    try:
        exec("from .%s import %s as tmp" % (package, type))
        module = locals()['tmp']
    except ImportError:
        raise NotImplementedError("installer for package %r, from %r" % (
            package, type))
    return module.get( version, platform = platform, pyver = pyver, **kwds )


def guess( package ):
    raise NotImplementedError


import os
# pwd = os.path.dirname( os.path.abspath( __file__ ) )
# releaser_root = os.path.abspath( os.path.join(pwd, '..', '..' ) )
releaser_root = os.path.abspath(os.curdir)
tarball_path = os.path.join(releaser_root, 'install-deps' )
if not os.path.exists( tarball_path ): os.makedirs( tarball_path )
if not os.path.isdir( tarball_path ): raise IOError("%r is not a directory" % tarball_path)

install_path = os.path.join( releaser_root, 'EXPORT', 'deps' )


def include_installed_dependencies():
    #allow access to installed python package
    depspythonpath = os.path.join(install_path, 'python')
    import sys
    sys.path = [depspythonpath] + sys.path
    os.environ['PYTHONPATH'] = '%s:%s' % (
        os.path.join(install_path, 'python'), 
        os.environ.get('PYTHONPATH') or '' )

    # easy install has special needs: it need to reload the special
    # site.py
    from . import easy_install_support
    easy_install_support.import_site()

    #update environ vars
    #bash only. bad hack...
    os.environ['PATH'] = '%s:%s' % (
        os.path.join( install_path, 'bin' ), os.environ['PATH'] )
    os.environ['LD_LIBRARY_PATH'] = '%s:%s' % (
        os.path.join( install_path, 'lib' ), os.environ.get('LD_LIBRARY_PATH') or '' )
    os.environ['DYLD_LIBRARY_PATH'] = '%s:%s' % (
        os.path.join( install_path, 'lib' ), os.environ.get('DYLD_LIBRARY_PATH') or '' )
    return

# the easy_install fix no longer works. have to run a fresh python session
# with new environment variables
# include_installed_dependencies()

from ..osutils import execute


# version
__id__ = "$Id$"

# End of file 
