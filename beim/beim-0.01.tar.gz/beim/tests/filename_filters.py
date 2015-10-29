#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def bypostfix(postfix='TestCase.py'):
    """return a test function that test if a filename is a test.
    the filter returned assumes that any filename ends with the given postfix
    is a good one.
    """
    def _(filename):
        return filename.endswith(postfix)
    return _


def byprefix(prefix='Test'):
    """return a test function that test if a filename is a test.
    the filter returned assumes that any module starts with the given prefix
    is a good one.
    """
    def _(filename):
        return filename.startswith(prefix)
    return _


def bypattern(pattern="test*.*"):
    """return a test function that test if a filename is a test.
    the filter returned assumes that any module matchs the given pattern
    is a good one.
    """
    import fnmatch
    def _(fn):
        return fnmatch.fnmatch(fn, pattern)
    return _


# version
__id__ = "$Id$"

# End of file 
