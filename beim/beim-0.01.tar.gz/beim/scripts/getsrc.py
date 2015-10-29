#!/usr/bin/env python
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


# script to check out sources

def get(names, pkgcontainer, tree):
    '''get sources of packages

    - names: a list of package names
    - pkgcontainer: the container of packages. must have the API defined in beim.packages.Packages
    - releaser_tree: directory tree structure of the releaser
    '''
    srcRt = tree.search( "sources" ).path
    
    import os
    if not os.path.exists(srcRt):
        os.makedirs(srcRt)
        os.system("bzr init-repo %s" % srcRt)
        pass
    
    if names:
        packages = [pkgcontainer.getPackage(n) for n in names]
    else:
        packages = pkgcontainer.getAll()
    from ..packages import checkout
    checkout(packages, srcRt)
    # import dereference
    # dereference.dereference_recursively( 'src' )
    return



def main():
    import packages
    from ..packages.factories import fromPyPackage
    pkgcontainer = fromPyPackage.factory(packages)

    from directory_structure import tree

    from optparse import OptionParser
    parser = OptionParser()
    (options, args) = parser.parse_args()
    names = args
    
    get(names, pkgcontainer, tree)
    return



# version
__id__ = "$Id$"

# End of file 
