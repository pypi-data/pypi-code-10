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

# make-Makemm.py <directory> <projectname>

# this module requires that the path to the root of the releaser to be included
# in PYTHONPATH

def main():
    import sys
    project = sys.argv[1]
    path = sys.argv[0]
    render(path, project)
    return


def render(path, project):
    import os
    
    d = { 'project': project }
    
    import packages
    packageInfoTable = getattr(packages, 'packageInfoTable', None)
    if packageInfoTable:
        # old "packages"
        table = packages.packageInfoTable

        dirs = []
        for name in packages.packageNames:
            info = table[name]
            dirs.append( info['path'] )
            continue
    else:
        # new oo "packages"
        from ..packages.factories.fromPyPackage import factory
        pkgs = factory(packages)
        pkgs = pkgs.getAll()
        dirs = [p.name for p in pkgs]

    dirs = ''.join( ['\t%s \\\n' % dir for dir in dirs] )
    d['directories'] = dirs
    
    pwd = os.path.abspath( __file__ )
    pwd = os.path.dirname( pwd )

    fmtstr = open( os.path.join( pwd, 'Make.mm.template' ) ).read()
    s = fmtstr % d

    f = os.path.join( path, 'Make.mm' )
    open( f, 'w' ).write( s )
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 


