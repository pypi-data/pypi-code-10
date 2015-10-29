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
from Passer import Passer
import _convenient_functions  as dsm


import journal
jrnltag = 'DataStreamModel'
warning = journal.warning( jrnltag )


class AmbiguousComponentSpecifier(Exception): pass


class Composite(Connectable):


    '''Support of connection of connectable to form a 
    composite connectable.
    '''
    
    def __init__(self, components, connections):
        '''__init__(connections, components) -> new composite connectable
  connections: a list of connections specified by strings
  components: a dictionary of {name:component} of components
      encapsulated in this composite
  '''
        Connectable.__init__(self)
        self._connections = connections
        self._components = components
        self._chains = self._establishConnections()
        return
        

    def _update(self):
        inputsPasser = self.inputsPasser
        outputsPasser = self.outputsPasser
        for k in self.sockets['in']:
            inputsPasser.setInput(k, self._getInput( k ) )
            continue
        
        chains = self._chains
        dsm.run( chains )
        
        for k in self.sockets['out']:
            self._setOutput(k, outputsPasser.getOutput( k ) )
            continue
        return 


    def _establishConnections(self):
        inputsPasser = Passer()
        outputsPasser = Passer()
                                     
        self.inputsPasser = inputsPasser
        self.outputsPasser = outputsPasser
        
        connections = self._connections

        ret = dsm.chains()
        
        for connection in connections:

            chain = dsm.chain( )
            
            for token in connection.split( '->' ):
                node = self._componentConnection( token )
                chain.append( node )
                continue

            ret.add( chain )
            continue
        
        return ret


    def _componentConnection(self, text):
        
        stext = text.split( ':' )
        
        if len(stext) == 2:

            t1, t2 = stext
            c1 = self._getComponent( t1 )
            c2 = self._getComponent( t2 )

            if c1 and c2:
                msg = \
                    'In %s: %s and %s are both resolvable'\
                    'as component names' % (
                    self, t1, t2 )
                raise AmbiguousComponentSpecifier, msg
                      
            if c1 is None and c2 is None:
                msg = \
                    "In component %s: "\
                    "No name resolvable to component: %s" % (
                    self, stext)
                raise msg

            if c1 is self: c1 = self.inputsPasser
            elif  c2 is self: c2 = self.outputsPasser
            
            if c1: return dsm.node( None, c1, t2 )

            return dsm.node( t1, c2, None )
                
        if len(stext) != 3:
            
            raise ValueError , \
                  "Invalid form: %s. "\
                  "Should be inputSocket:componentName:outputSocket"\
                  % (text)
        
        inSocket, compName, outSocket = stext
        
        component = self._getComponent( compName )

        return dsm.node( inSocket, component, outSocket )
    

    def _getComponent( self, name ):
        if name == 'self': return self
        try: return self._components[ name ]
        except:
            warning.log( "Unknown component: %s" % name )
            return

    pass # end of Composite


def main():
    from Connectable import Connectable
    class Adder(Connectable):

        sockets = {
            'in': [ 'operand1', 'operand2' ],
            'out': ['return'],
            }

        def _update(self):
            inputs = self._inputs
            self._outputs['return'] = inputs['operand1'] + inputs['operand2']
            return

        pass

        
    class Multiplier(Connectable):

        sockets = {
            'in': [ 'operand1', 'operand2' ],
            'out': ['return'],
            }

        def _update(self):
            inputs = self._inputs
            self._outputs['return'] = inputs['operand1'] * inputs['operand2']
            return

        pass


    class DSMExample(Composite):

        sockets = {
            'in': [ '1','2','3' ],
            'out': [ 'return' ],
            }

        
        def __init__(self):

            connections = [
                'self:1->operand1:adder',
                'self:2->operand2:adder',
                'self:3->operand1:multiplier',
                'adder:return->operand2:multiplier',
                'multiplier:return->return:self',
                ] 

            adder = Adder() 
            multiplier = Multiplier()
            components = {
                'adder': adder,
                'multiplier': multiplier,
                }
            Composite.__init__(self, components, connections)
            return

        pass # end of DSMExample
            
    dsmexample = DSMExample()
    dsmexample.setInput( '1', 5 )
    dsmexample.setInput( '2', 6 )
    dsmexample.setInput( '3', 8 )
    assert dsmexample.getOutput( 'return' )==(5+6)*8
    return


warning.deactivate()


if __name__ == '__main__': main()
        

# version
__id__ = "$Id$"

# End of file 
