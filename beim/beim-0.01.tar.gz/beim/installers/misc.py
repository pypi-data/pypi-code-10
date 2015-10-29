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


dynamicloadedlibrary_exts = {
    'darwin': 'dylib',
    'linux2': 'so',
    'cygwin': 'so',
    }


import sys
so = dynamicloadedlibrary_exts[ sys.platform ]


# version
__id__ = "$Id$"

# End of file 
