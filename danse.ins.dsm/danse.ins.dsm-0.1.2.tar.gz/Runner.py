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


import journal
info = journal.info( 'dsm.Runner' )


class Runner:


    def __call__(self, runable, stream = None):
        self.stream = stream
        return runable.identify(self)


    def onChains(self, chains):
        for chain in chains: chain.identify(self)
        return


    def onChain(self, chain):
        for node in chain:
            self.onNode( node )
            if node is not chain.last():
                self.onConnection( (node, node.next) )
                pass
            continue
        return


    def onNode(self, node):
        # node is an instance of Node
        inSocket = node.inSocket
        component = node.component
        outSocket = node.outSocket

        info.log( "Send %s to socket %s of component %s" % (
            self.stream, inSocket, component) )
        if inSocket: component.setInput( inSocket, self.stream )

        info.log( "Component %s is running" % (component,))
        if outSocket: self.stream = component.getOutput( outSocket )

        info.log( "Retrive output from socket %s of component %s: %s" % (
            outSocket, component, self.stream) )
        return
    
    
    def onConnection(self, connection ):
        '''pass stream along the connection establish
        '''
        #self.stream = ...
        #trivial implementation
        return 


    pass # end of Runner



def test():
    from Connectable import Connectable
    class A(Connectable):
        sockets = {
            'out': ['1'],
            }
        def _update(self):
            self._outputs['1'] = 1
            return
        pass
    a = A()
    
    from Passer import Passer
    class B(Passer):
        sockets = {
            'in': ['1'],
            'out': ['1'],
            }
        pass
    b = B()

    class C(Connectable):
        sockets = {
            'in': ['in3'],
            'out': ['out'],
            }
        def _update(self):
            self._outputs['out'] = self._inputs['in3']
            return
        pass
    c = C()
    
    from Node import Node
    n1 = Node( None, a, '1' )
    n2 = Node( '1', b, '1' )
    n3 = Node( 'in3', c, None )
    
    from Chain import Chain
    ch = Chain()
    ch.append( n1 )
    ch.append( n2 )
    ch.append( n3 )
    
    from Chains import Chains
    cs = Chains()
    cs.add( ch )

    r = Runner()
    r( cs )

    assert c.getOutput( 'out' ) == 1
    return


def main():
    test()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
