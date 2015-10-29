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


"""
sub-packages:

* build: find out dependencies, create .tools, and build
* installers: installers for dependent software packages
* envvars: environment variable manipulations
* paths: utilities to find out installation paths of software packages
* scripts: provide methods that can be used as the 'main' method of useful scripts

"""


def make_tarball( directory ):
    """make a tarball of the given directory tree.
    
    make_tarball( "/a/b/c/hello" ) --> hello.tgz
    """
    import os
    name = os.path.basename( directory )
    tarball = '%s.tgz' % name
    
    import tarfile
    f = tarfile.open( tarball, 'w:gz' )
    f.add( directory, name )
    del f
    
    return tarball



# version
__id__ = "$Id$"

# End of file 
