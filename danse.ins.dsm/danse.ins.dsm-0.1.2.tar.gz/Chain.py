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


class Chain:
    
    
    def __init__(self):
        self._sequence = []
        return


    def last(self): return self._sequence[-1]
    
    
    def append(self, node):
        try:
            end = self._sequence[-1]
            end.next = node
        except:
            pass
        self._sequence.append(node)
        return
    
    
    def __iter__(self):
        return self._sequence.__iter__()


    def identify(self, visitor): return visitor.onChain(self)
        
    
    pass # end of Chain


# version
__id__ = "$Id$"

# End of file 
