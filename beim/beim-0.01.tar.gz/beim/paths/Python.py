"""
handle paths for python itself
"""

name = "python"
description = 'python itself'


from distutils import sysconfig
import sys
import os

from .PathsFinder import PathsFinder

class PythonPaths(PathsFinder):

    mechanism = "extract python includes and libs using distutils module sysconfig"
    
    def extract(self):
        """
        extract my paths from sysconfig, which is a module in distutils
        """
        something = self._hintsToFindPaths
        derivedFrom = self._derivedFrom
        
        if something is None: something = sysconfig
        include_dirs = []
        # Make sure Python's include directories (for Python.h, pyconfig.h,
        # etc.) are in the include search path.
        py_include = something.get_python_inc()
        plat_py_include = something.get_python_inc(plat_specific=1)

        # Put the Python "system" include dir at the end, so that
        # any local include dirs take precedence.
        include_dirs.append(py_include)
        if plat_py_include != py_include:
            include_dirs.append(plat_py_include)
            pass

        library_dirs = [ something.get_config_var( 'LIBDEST' ) ]
        runtimelib_dirs = []

        # for extensions under windows use different directories
        # for Release and Debug builds.
        # also Python's library directory must be appended to library_dirs
        if os.name == 'nt':
            library_dirs.append(os.path.join(sys.exec_prefix, 'libs'))

            # Append the source distribution include and library directories,
            # this allows distutils on windows to work in the source tree
            include_dirs.append(os.path.join(sys.exec_prefix, 'PC'))
            library_dirs.append(os.path.join(sys.exec_prefix, 'PCBuild'))
            pass

        # OS/2 (EMX) doesn't support Debug vs Release builds, but has the 
        # import libraries in its "Config" subdirectory
        if os.name == 'os2':
            library_dirs.append(os.path.join(sys.exec_prefix, 'Config'))
            pass

        # for extensions under Cygwin and AtheOS Python's library directory must be
        # appended to library_dirs
        if sys.platform[:6] == 'cygwin' or sys.platform[:6] == 'atheos':
            if str.find(sys.executable, sys.exec_prefix) != -1:
                # building third party extensions
                library_dirs.append(
                    os.path.join(sys.prefix, "lib",
                                 "python" + get_python_version(),
                                 "config"))
                pass
            else:
                # building python standard extensions
                library_dirs.append('.')
                pass
            pass

        root = None; modules = None
        #for windows nt we may want to know root and site-packages
        if os.name == "nt": 
            from .NTPythonRoot import pythonInstallationPath as root
            modules = [os.path.join(root, "Lib", "site-packages")]

        #config dir
        config_dir = something.get_config_var( 'LIBPL' )

        from .Paths import Paths
        ret = Paths(
            self.name,
            root = root,
            includes= include_dirs,
            clibs= library_dirs,
            modules= modules,
            description = self.description,
            origin = self.mechanism)
        ret.config_dir = config_dir
        return ret
        



def find():
    toolset = [PythonPaths(name, description, hints = None)]
    from .search import search
    return search(toolset)
