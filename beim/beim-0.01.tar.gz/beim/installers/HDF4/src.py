name = 'HDF'
server = 'ftp://ftp.hdfgroup.org/HDF/prev-releases'

def get( version = None, **kwds ):
    if version is None: version = "4.2r1"
    identifier = '%s%s' % (name, version)
    cmds = [
         #we don't need fortran library, right?
        'LDFLAGS=-lm ./configure --prefix=$PREF  --with-jpeg=$PREF --with-szip=$PREF --with-zlib=$PREF --enable-fortran=no',
        'make',
        'make install',
        ]
    def _():
        install( name, version,
                 identifier = identifier, server = server,
                 install_commands = cmds,
                 **kwds )
        import os
        os.environ['HDF4_DIR'] = install_path
        return
    return _
    

from ..src import install, install_path

