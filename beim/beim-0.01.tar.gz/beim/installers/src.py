
from . import tarball_path, install_path, execute
from .download import download_cmd

def install( name,
             version = None,  revision = None,
             server = None, identifier = None,
             install_commands = [],
             tarball_ext = 'tar.gz',
             tarball_extraction_cmd = None,
             **kwds ):
    if identifier is None:
        identifier = '%s-%s' % (name, version,)
        pass
    tarball = "%s.%s" % (identifier, tarball_ext)
    link = '%s/%s' % (server, tarball )
    path = identifier
    if tarball_extraction_cmd is None:
        tarball_extraction_cmd = _guess_tarball_extraction_cmd( tarball_ext )
    
    cmds = [
        'cd %s' % tarball_path,
        'rm -rf %s' % path,
        'rm -rf %s' % tarball,
        ] + \
        download_cmd( link ) + [\
        '%s %s' % (tarball_extraction_cmd, tarball),
        'cd %s' % path,
        ]
    cmds += install_commands
    cmd = ' && '.join(cmds)
    execute(cmd)
    return


_tarball_extraction_cmds = {
    'tar.gz': 'tar zxvf',
    'tar.bz2': 'tar jxvf',
    }
def _guess_tarball_extraction_cmd( ext ):
    return _tarball_extraction_cmds[ ext ]
