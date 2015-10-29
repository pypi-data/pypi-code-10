#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class InstallationNotFound( Exception ):

    def __init__(
        self,
        packagename=None,
        errormessage=None,
        packageid=None,
        possible_solution=None):
        
        self.packagename = packagename
        self.errormessage = errormessage
        self.packageid = packageid
        self.possible_solution = possible_solution
        
        return


# version
__id__ = "$Id$"

# End of file 
