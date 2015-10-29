# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
test dir configuration file: .tests.beimconfig   (see TestHarness)
configuration file format:

configuration file is a python module. (see config_utils)

it could define the following parameter:

* testfile_filter
 Examples:
 >>> testfile_filter = filename_filters.byprefix("test")
 >>> testfile_filter = filename_filters.bypattern("test*.cc")
 

"""


# version
__id__ = "$Id$"

# End of file 
