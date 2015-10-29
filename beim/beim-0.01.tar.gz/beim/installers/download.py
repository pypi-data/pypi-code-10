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


def download_cmd( link ):
    if link.startswith( 'http:' ) or link.startswith( 'ftp:'):
        return [ 'wget %s' % link ]
    elif link.startswith( 'svn:' ):
        return download_using_svn( link )
    else:
        raise NotImplementedError

def download_using_svn( link ):
    # a temporary directory
    import tempfile
    tempdir = tempfile.mkdtemp()
    
    import os
    path, filename = os.path.split( link )
    dirname = os.path.split( path )[-1]
    cmds = [
        # save current path
        'tempvar_current_path=$PWD',
        # go into the temp dir
        'cd %s' % tempdir,
        # check out directory
        'svn co -N %s' % path,
        # cd into the directory and get file
        'cd %s' % dirname,
        'svn up %s' % filename,
        # mv file back
        'mv %s $tempvar_current_path' % filename,
        # go back
        'cd $tempvar_current_path',
        # remove directory
        'rm -rf %s' % tempdir,
        ]
    return cmds


# version
__id__ = "$Id$"

# End of file 
