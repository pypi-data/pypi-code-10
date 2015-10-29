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

# texcommon of danse. it contains of style files used by danse.
# env var: DANSE_TEXCOMMON_DIR

def render( paths ):
    lines = [
        "export DANSE_TEXCOMMON_DIR='%s'" % paths.root,
        ]
    return lines
        

# version
__id__ = "$Id$"

# End of file 
