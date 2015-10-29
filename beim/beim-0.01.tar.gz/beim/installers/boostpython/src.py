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


name = 'boostpython'
server = 'http://downloads.sourceforge.net/project/boost/boost/1.35.0'

def get( version = None, **kwds ):
    name = 'boost'
    if version is None: version = "1_35_0"
    identifier = "%s_%s" % (name, version)
    
    install_cmds = [
        './configure --prefix=%s --with-libraries=python' %  (install_path,),
        'make install',
        ]

    from ..misc import so
    postinstall_cmds = [
        'cd %s/include' % (install_path,),
        'ln -s `ls -1|grep boost`/boost %(name)s' % {
        'name': name,
        'version': version,
        },
        ]

    cmds = install_cmds + postinstall_cmds

    def _():
        install(
            name, version,
            identifier = identifier,
            server = server,
            install_commands = cmds,
            **kwds )

        # libboost_python.so
        import glob, os
        files = glob.glob('%s/lib/libboost_python*.so.*' % install_path)
        file0 = files[0]
        os.symlink(file0, '%s/lib/libboost_python.so' % install_path)
        
        # notification
        import os
        os.environ['BOOSTPYTHON_DIR'] = install_path
        
        return
    
    return _
    

from ..src import install, install_path



# version
__id__ = "$Id$"

# End of file 
