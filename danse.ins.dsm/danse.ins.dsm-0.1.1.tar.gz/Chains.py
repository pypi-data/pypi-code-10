#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Chains:

    def __init__(self):
        self._store = []
        return


    def __iter__(self): return self._store.__iter__()


    def add(self, chain): self._store.append( chain)


    def identify(self, visitor): return visitor.onChains(self)


    pass # end of Chains

# version
__id__ = "$Id$"

# End of file 
