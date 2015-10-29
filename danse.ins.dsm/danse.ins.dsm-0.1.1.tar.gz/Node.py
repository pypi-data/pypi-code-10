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


class Node:

    def __init__(self, inSocket, component, outSocket ):
        #component should be an instance of Connectable
        self.inSocket = inSocket
        self.component = component
        self.outSocket = outSocket
        return


    pass # end of Node


# version
__id__ = "$Id$"

# End of file 
