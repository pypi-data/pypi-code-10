# -*- python -*-
# Jiao Lin
# Caltech


# perform the operations

class Performer(object):

    def render(self, operations):
        for op in operations:
            op.identify(self)
            continue
        return 


    def onSet(self, op):
        os.environ[op.name] = op.value


    def onAppend(self, op):
        old = os.environ.get(op.name)
        if old:
            new = '%s:%s' % (old, op.value)
        else:
            new = op.value
        os.environ[op.name] = new


    def onPrepend(self, op):
        old = os.environ.get(op.name)
        if old:
            new = '%s:%s' % (op.value, old)
        else:
            new = op.value
        os.environ[op.name] = new


import os

# $Id: Performer.py 535 2010-11-07 04:48:00Z linjiao $
# end of file
