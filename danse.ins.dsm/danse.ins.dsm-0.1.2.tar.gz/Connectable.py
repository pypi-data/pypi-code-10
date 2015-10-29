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


class InvalidSocket(Exception): pass

class Connectable:

    sockets = {
        'in': [ ],
        'out': [ ],
        }

    def __init__(self):
        self._inputs = {}
        self._outputs = {}
        self._consumedInputs = self._inputs.copy()
        return
    
    
    def setInput(self, name, value):
        if name not in self.sockets['in']:
            raise InvalidSocket , "%s, Unknown input socket: %s" % (
                self, name)
        self._inputs[name] = value
        return

        
    def getOutput(self, name):
        if name not in self.sockets['out']:
            raise InvalidSocket , "%s, Unknown output socket: %s" % (
                self, name)
        self._updateIfNecessary()
        return self._outputs[name]


    def __str__(self):
        return self.__class__.__name__

    
    def _update(self):
        raise NotImplementedError, "%s" % self.__class__


    def _getInput(self, name):
        '''only useful for friendly class'''
        return self._inputs[name]


    def _setOutput(self, name, value):
        '''only useful for friendly class'''
        self._outputs[name ] = value
        return
    

    def _updateIfNecessary(self):
        if self._consumedInputs == self._inputs and self._outputs != {}: return
        self._update()
        self._consumedInputs = self._inputs.copy()
        return

    pass # end of Connectable


# version
__id__ = "$Id$"

# End of file 
