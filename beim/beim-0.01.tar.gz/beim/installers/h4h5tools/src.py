name = 'h4h5tools'
server = 'ftp://ftp.hdfgroup.org/HDF5/h4toh5'

def get( version = None, **kwds ):
    if version is None: version = "1.2"
    cmds = [
        'CC=%s/bin/h4cc ./configure --prefix=%s --with-hdf5=%s' % (
        install_path, install_path, install_path ),
        'make',
        'make install',
        ]
    def _():
        install( name, version,
                 server = server,
                 install_commands = cmds,
                 **kwds )
        return
    return _
    

from ..src import install, install_path

