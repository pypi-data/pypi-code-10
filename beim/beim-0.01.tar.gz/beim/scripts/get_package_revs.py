#!/usr/bin/env python
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


def main(packages):
    from beim.packages.factories import fromPyPackage
    pkgcontainer = fromPyPackage.factory(packages)
    
    for pkg in pkgcontainer.getAll():
        rev = pkg.getRevision()
        print('* %s: %s' % (pkg.name, rev))
    return


# version
__id__ = "$Id$"

# End of file 
