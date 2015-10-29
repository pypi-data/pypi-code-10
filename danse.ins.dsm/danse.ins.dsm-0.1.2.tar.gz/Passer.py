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


from Connectable import Connectable

class Passer( Connectable ):

    '''trivial connectable'''

    def __init__(self):
        Connectable.__init__(self)
        return
    

    def setInput(self, name, value):
        self._inputs[name] = value
        return

        
    def getOutput(self, name):
        return self._inputs[name]

    pass # end of Passer
    

# version
__id__ = "$Id$"

# End of file 
