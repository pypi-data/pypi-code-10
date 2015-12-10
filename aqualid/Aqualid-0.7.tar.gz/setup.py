
import os
import errno

from distutils.core import setup
from distutils.command.install_scripts import install_scripts

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)


# ==============================================================================
def   _removeFile( file ):
  try:
    os.remove( file )
  except OSError as ex:
    if ex.errno != errno.ENOENT:
      raise

class InstallScripts( install_scripts ):

  def   __getInstallDir(self):

    # use local imports as a workaround for multiprocessing and run_setup
    import os.path
    import site

    install_dir = os.path.normcase( os.path.abspath(self.install_dir) )
    sys_prefix = os.path.normcase( site.USER_BASE )

    if not install_dir.startswith( sys_prefix ):
      return os.path.abspath( os.path.join( self.install_dir, '..' ) )

    return None

  def run(self):
    # use local imports as a workaround for multiprocessing and run_setup
    import os
    from distutils.command.install_scripts import install_scripts

    install_scripts.run( self )

    if os.name == 'nt':
      install_dir = self.__getInstallDir()
      if install_dir:
        for script in self.get_outputs():
          if script.endswith( ('.cmd','.bat') ):
            dest_script = os.path.join(install_dir, os.path.basename(script))
            _removeFile( dest_script )
            self.move_file( script, dest_script )

if os.name == 'nt':
  scripts = [ 'scripts/aql.cmd']
else:
  scripts = [ 'scripts/aql']

LONG_DESCRIPTION = """
Aqualid
=======

General purpose build tool.

Key features:
  - Flexible and scalable for large projects
  - Dynamic dependency graph
  - Batch build support
  - Distributed build scripts (no fixed project structure)
  - Support any build target types (files, strings, URLs, remote resources etc.)
  - Conditional options
  - Scons like build scripts (but not compatible)
"""

setup(
      name              = 'Aqualid',
      version           = '0.7',
      author            = 'Constanine Bozhikov',
      author_email      = 'voidmb@gmail.com',
      description       = 'General purpose build system.',
      long_description  = LONG_DESCRIPTION,
      url               = 'https://github.com/aqualid',
      license           = 'MIT License',
      platforms         = "All platforms",
      scripts           = scripts,
      package_dir       = {'': 'modules'},
      packages          = ['aqualid'],
      package_data      = {'aqualid': ['tools/*']},
      cmdclass          = { 'install_scripts' : InstallScripts,}
)
