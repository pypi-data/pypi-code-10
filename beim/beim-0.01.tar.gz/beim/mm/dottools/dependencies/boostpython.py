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
    lines = [
        "export BOOSTPYTHON_LIBDIR='%s'" % libdir,
        "export BOOSTPYTHON_INCDIR='%s'" % incdir,
        ]
    return lines
        

# version
__id__ = "$Id$"

# End of file 
