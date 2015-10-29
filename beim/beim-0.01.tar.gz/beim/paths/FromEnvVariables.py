__doc__ = """search paths of a package by using system environment variables."""
__author__ = "Jiao Lin"

from .PathsFinder import PathsFinder as base
import os,sys
from .envUtils import getEnv

class PathsFinder(base):

    """search paths of a package by using system environment variables.
    
    For example, we could know the installation tree of matlab if user set the
    environment variable MATLAB_DIR, which is the path to the root of installation
    tree of matlab.

    In unix-like system, a package is usually installed with such a structure
    -  /usr.............root
    -  /usr/include.....header
    -  /usr/lib.........libs
    So we have a default scheme reflecting this structure. We also added a sub directory
    "python" to this default structure.

    We allow users to overload this structure easily by provide more detailed
    information through environment variables. For example, a user can specify
    env variable
    - MATLAB_INCDIR
    by doing something like
    - $ export MATLAB_INCDIR=/usr/local/include
    to tell us the path to Matlab headers.

    We allow programmers to overload this structure easily by overloading the member
    variable
    - scheme

    We also allow programmers to overload the names of the envrionment variables
    that can be used by users to overload the directory structure by overloading
    the member variable
    - env_var_scheme
    """

    mechanism = "search paths of a package by using system environment variables"

    #scheme is used to determine the positions of subdirectories of a package
    if os.name == "posix":
        scheme = {'root': '.',
                  'c headers': 'include',
                  'c libraries': 'lib',
                  'python modules': 'python'}
    #windows is different
    elif os.name == "nt":
        scheme = {'root': '.',
                  'c headers': 'Include',
                  'c libraries': 'libs',           #I supposed dll libraries are installed into sth like c:\python\libs, too
                  'python modules': 'Lib\\site-packages'}
    else :
        raise NotImplementedError("Don't know how to determine default installation scheme for %s, %s" % (os.name, sys.platform))


    #env_var_scheme is used to 
    env_var_scheme = {
        'root': '_DIR',
        'c headers': '_INCDIR',
        'c libraries': '_LIBDIR',
        'python modules': '_PYTHONDIR'}
    

    def _extract(self):
        """
        extract my paths from system environment variables

        variableName:   base name of the environment variable 
        derivedFrom:    name of the package from which the paths of this package could be derived
        """
        variableName = self._hintsToFindPaths
        derivedFrom  = self._derivedFrom
        
        from os.path import join

        self.variableName = variableName

        self.env_variable_names = self._getEnvVarNames(variableName)
        
        base_desc = self.description
        desc_format_str = 'path to %s directory of ' + base_desc
        
        self.root = root = self._getRoot(desc_format_str, derivedFrom)
        include = self._getEnv('c headers', desc_format_str)
        clib = self._getEnv('c libraries', desc_format_str)
        python = self._getEnv('python modules', desc_format_str)
                           
        from .Paths import Paths
        return Paths( self.name,
                      root=root,
                      includes=[include],
                      clibs=[clib],
                      modules=[python],
                      description = self.description,
                      origin = self.mechanism,)


    def _getEnvVarNames( self, variable_name):
        "use self.env_var_scheme to determine the names of environment variables"
        scheme = self.env_var_scheme
        res = {}
        for key, value in scheme.items():
            res[key] = '%s%s' % (variable_name, value)
            continue
        return res


    def _getRoot(self, desc_format_str, derivedFrom):
        "get path to the root"
        #
        rootEnvVar = self.env_variable_names['root']
        desc = desc_format_str % " root"
        #
        if derivedFrom is None: default = None
        else : default = self.getPaths(derivedFrom).root
        #
        return  getEnv( rootEnvVar, default, desc )

    
    def _getEnv( self, type, desc_format_str ):
        return getEnv( self.env_variable_names[type],
                       _getDefaultDir( self.root, self.scheme[type]),
                       desc_format_str % type)
    

  
def _getDefaultDir( packageDir, subDir ):
    import os
    if subDir: return os.path.join( packageDir, subDir )
    else : return None
