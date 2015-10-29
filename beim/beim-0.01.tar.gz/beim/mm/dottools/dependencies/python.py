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

def render( paths ):
    libdir = paths.clibs[0]
    incdir = paths.includes[0]
    config_dir = paths.config_dir
    lines = [
        "export PYTHON_LIBDIR='%s'" % libdir,
        "export PYTHON_INCDIR='%s'" % incdir,
        "export PYTHON_CONFIGDIR='%s'" % config_dir,
        ]
    return lines
        

# version
__id__ = "$Id$"

# End of file 
