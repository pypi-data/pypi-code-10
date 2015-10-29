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


name = 'h5py'
server = "http://h5py.googlecode.com/files"
#http://code.google.com/p/h5py/downloads/detail?name=h5py-1.3.0.tar.gz

def get( version = None, **kwds ):
    if version is None: version = "1.3.0"
    install_pythonpath = '%s/python' % install_path
    import os
    if not os.path.exists(install_pythonpath): os.makedirs(install_pythonpath)
    cmd = 'python setup.py install --prefix=%s --install-lib=%s' % (
        install_path, install_pythonpath)
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
