#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                    Jiao Lin
#                        California Institute of Technology
#                           (C) 2006 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


# adapted from Michael Aivazis's Singleton

# adapted from GvR's Singleton implementation

class SingletonByName(object):


    def __new__(cls, name, *args, **kwds):
        its = cls.__dict__.get("__its__")
        if its is None:
            its = cls.__its__ = {}
        try:
            return its[name]
        except KeyError:
            new_inst = object.__new__(cls)
            its[name] = new_inst
            return its[name]


    def getSingleton(self, name):
        return self.__class__.__dict__.get("__its__")[name]



# version
__id__ = "$Id: SingletonByName.py 135 2005-08-06 16:31:39Z linjiao $"

#  End of file 
