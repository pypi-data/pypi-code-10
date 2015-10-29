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


name = 'matplotlib'
server = 'http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-0.99'
#http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-0.99/matplotlib-0.99.0.tar.gz
#http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-0.99.1/matplotlib-0.99.1.2.tar.gz

def get( version = None, **kwds ):
    if version is None: version = "0.99.0"
    cmds = [
        "python setup.py install --prefix=%s --install-lib=%s/python" % (
        install_path, install_path ),
        ]
    def _():
        install( name, version,
                 server = server, install_commands = cmds,
                 **kwds )
        return
    return _
    

from ..src import install, install_path



# version
__id__ = "$Id$"

# End of file 
