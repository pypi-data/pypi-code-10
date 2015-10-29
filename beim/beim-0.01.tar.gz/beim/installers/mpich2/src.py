name = 'mpich2'
server = 'http://www.mcs.anl.gov/research/projects/mpich2/downloads/tarballs/1.0.8p1'

def get( version = None, **kwds ):
    if version is None: version = "1.0.8p1"
    cmds = [
        './configure --prefix=%s --enable-sharedlibs=gcc' % install_path,
        'make',
        'make install',
        ]
                        
    def _():
        install( name, version,
                 server = server,
                 install_commands = cmds,
                 **kwds )
        import os
        os.environ['MPICH2_DIR'] = install_path
        return
    
    return _
    

from ..src import install, install_path

