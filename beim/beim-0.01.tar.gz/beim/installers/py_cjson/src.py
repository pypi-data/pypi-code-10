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


name = 'python-cjson'
server = 'http://pypi.python.org/packages/source/p/python-cjson/'

def get( version = None, **kwds ):
    if version is None: version = "1.0.5"
    cmd = 'python setup.py install --prefix=%s --install-lib=%s/python' % (
        install_path, install_path)
    def _():
        return install(
            name, version,
            server = server,
            install_commands = [cmd],
            **kwds )
    return _
    

from ..src import install, install_path



# version
__id__ = "$Id$"

# End of file 
