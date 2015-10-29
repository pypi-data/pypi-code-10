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


name = 'wxPython'
#server = 'svn://danse.us/buildInelast/external/wxPython/2.8.4.0/src'
server = 'http://downloads.sourceforge.net/project/wxpython/wxPython/2.8.10.1'

def get( version = None, **kwds ):
    if version is None: version = "2.8.10.1"
    identifier = '%s-src-%s' % (name, version)
    
    Args="BUILD_GLCANVAS=0"
    
    cmds = [
        './configure --enable-monolithic --prefix=%s' % install_path,
        'make',
        #'make -C contrib/src/animate',
        'make -C contrib/src/gizmos',
        'make -C contrib/src/stc',
        'make install',
        #'make -C contrib/src/animate install',
        'make -C contrib/src/gizmos install',
        'make -C contrib/src/stc install',
        'cd %s' % name,

        # Does --inplace do something useful?
        'python setup.py build_ext --inplace %s' % Args,
        # Do not specify --root= here; it's picking it up from somewhere else
        'python setup.py install %s  --prefix=%s --install-lib=%s/python' % (
        Args, install_path, install_path)
        ]
    
    def _():
        install( name, version,
                 server = server, 
                 identifier = identifier,
                 tarball_ext = 'tar.bz2',
                 install_commands = cmds,
                 **kwds )
        return
    return _
    

from ..src import install, install_path



# version
__id__ = "$Id$"

# End of file 
