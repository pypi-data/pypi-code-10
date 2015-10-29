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


def run( runnable, stream = None ):
    from Runner import Runner
    r = Runner()
    return r( runnable, stream )


def node(inSocket, component, outSocket):
    from Node import Node
    return Node( inSocket, component, outSocket )


def composite( components, connections ):
    from Composite import Composite
    return Composite( components, connections )


def chain():
    from Chain import Chain
    return Chain()


def chains():
    from Chains import Chains
    return Chains()


# version
__id__ = "$Id$"

# End of file 
