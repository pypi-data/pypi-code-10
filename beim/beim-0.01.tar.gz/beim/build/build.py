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

# this module requires that the path to the root of the releaser to be included
# in PYTHONPATH


def run(
    projectname, src_root, export_root, build_root, merlin_dir,
    arguments = []
    ):
    # prepare
    dottools = prepare(
        projectname, src_root, export_root, build_root, merlin_dir,
        )
    # run mm
    runmm( src_root, dottools, arguments = arguments )
    return


def prepare(
    projectname, src_root, export_root, build_root, merlin_dir,
    ):
    '''
    prepare for build
    
    tmp_root: temporary directory
    src_root: root of sources where Make.mm will be put and mm will be run
    export_root: path where libraries, python modules, ... will be exported
    '''
    
    import os

    #create Make.mm
    from . import generate_Makemm
    generate_Makemm.render( src_root, projectname )
    
    #create dottools
    from . import generate_dottools
    dottools = generate_dottools.render(
        src_root, export_root, build_root, merlin_dir )

    # create directories
    if not os.path.exists( build_root ): os.makedirs( build_root )
    return dottools


def runmm( path, dottools, arguments = []):
    cmd = "bash -c '. %(dottools)r && mm %(args)s'" % {
        'dottools': dottools,
        'args': ' '.join( arguments ),
        }
    # save current directory
    import os
    pwd = os.path.abspath( os.curdir )
    
    # change to build dir
    os.chdir( path )

    # run
    if os.system(cmd): raise RuntimeError("%s failed" % cmd)

    # change back to original directory
    os.chdir( pwd )

    return
    

from .generate_dottools import DependencyMissing

# version
__id__ = "$Id$"

# End of file 


