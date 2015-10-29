#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def render_header( target, export_root, build_root, merlin_dir ):
    lines = render_target(target)
    lines += render_export_root( export_root )
    lines += render_build_root( build_root )
    lines += render_merlin_path( merlin_dir )
    # XXX: is this a good idea? default compiler would be gcc
    lines.append('export COMPILER=gcc')
    return lines


def render_dependency( dep ):
    '''render strings for setting environ vars for the given dependency

    e.g. render_dependency("mpich2")
    '''
    paths = getpaths( dep )
    from .dependencies import render
    return render(paths)
    

def render_target( target ):
    return ['export TARGET=%s' % target]


def render_export_root( export_root ):
    return ['export EXPORT_ROOT="%s"' % export_root]


def render_build_root( build_root ):
    return ['export BLD_ROOT="%s"' % build_root]


def render_merlin_path( merlin_dir ):
    return [
        'export PATH=%s/bin:${PATH}' % merlin_dir,
        'export PYTHONPATH=%s/packages:${PYTHONPATH}' % merlin_dir,
        # 'export BLD_CONFIG="%s"' % config_dir,
        ]


from ...paths import get as _getpaths
def getpaths( package ):
    paths = getpathsInInstalledDependencies( package )
    if paths: return paths
    return _getpaths( package )


def getpathsInInstalledDependencies( package ):
    '''get paths of a package assuming it is in "deps" directory
    of this releaser'''
    var = '%s_DIR' % package.upper()
    import os
    save = os.environ.get( var )

    from ...installers import install_path
    os.environ[ var ] = install_path

    try: ret = _getpaths( package )
    except: ret = None

    if save: os.environ[ var ] = save
    
    return ret



# version
__id__ = "$Id$"

# End of file 
