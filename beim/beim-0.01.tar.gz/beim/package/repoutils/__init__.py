#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def getRevision(pkgrepo):
    h = _h(pkgrepo, 'getRevision')
    return h(pkgrepo)


def _h(pkgrepo, key):
    m = _m(pkgrepo)
    return getattr(m, key)


def _m(pkgrepo):
    type = pkgrepo.type
    return globals()[type]


from . import svn, bzr


# version
__id__ = "$Id$"

# End of file 

