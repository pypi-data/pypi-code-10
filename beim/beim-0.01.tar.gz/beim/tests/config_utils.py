# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
utilities for loading test configuration
 
"""



def load(path):
    "load configuration from a file"
    env = {}
    from . import filename_filters
    env['filename_filters'] = filename_filters
    
    s = open(path).read()
    exec(s, env)
    
    return env


# version
__id__ = "$Id$"

# End of file 
