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


# script to update sources

def update(names, pkgcontainer, tree):
    '''update sources of packages

    - names: a list of package names
    - pkgcontainer: the container of packages. must have the API defined in beim.packages.Packages
    - releaser_tree: directory tree structure of the releaser
    '''
    srcRt = tree.search( "sources" ).path
    if names:
        packages = [pkgcontainer.getPackage(n) for n in names]
    else:
        packages = pkgcontainer.getAll()
    from ..packages import update
    update(packages, srcRt) #, dry_run=1)
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
    
    update(names, pkgcontainer, tree)
    return



# version
__id__ = "$Id$"

# End of file 
