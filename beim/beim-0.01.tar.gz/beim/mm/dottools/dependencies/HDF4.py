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
    root = paths.root
    libdir = paths.clibs[0]
    incdir = paths.includes[0]
    lines = [
        "export HDF4_DIR='%s'" % root,
        "export HDF4_LIBDIR='%s'" % libdir,
        "export HDF4_INCDIR='%s'" % incdir,
        ]
    return lines
        

# version
__id__ = "$Id$"

# End of file 
