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

# *** both implementations here do not seem to work

def import_site():
    #site.py is used by easy_install to fix sys.path
    #it needs to be reloaded sometimes.
    try:
        import site
    except ImportError:
        return
    
    # reload(site)
    return


def import_site(path):
    import imp
    name = 'site'
    file, filename, desc = imp.find_module(name, [path])
    # imp.load_module(name, file, filename, desc)
    m = imp.load_module('t', file, filename, desc)
    m.__boot()
    return



# version
__id__ = "$Id$"

# End of file 
