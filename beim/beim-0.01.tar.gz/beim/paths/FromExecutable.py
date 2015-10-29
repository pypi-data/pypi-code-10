__doc__ = """search paths of a package by using system environment variables."""
__author__ = "Jiao Lin"


from .PathsFinder import PathsFinder as base


from .envUtils import get_usingExec
from .shutils import env
from ._utils import findpackage


class PathsFinder(base):

    """
    search paths of a package by looking for executable.

    This special path finder search for a package by looking for the typical executable
    of a package. For example, to look for package matlab, we look for the executable
    "matlab". Currently this is done by Mike Mckerns' infect/utils.py. Then the root
    directory of the package is assumed to be in "..". The "scheme" is then applied to
    find directories containing headers and libraries, etc.

    Moreover, more complex methods to find subdirectories of a package can be used.
    for example, Matlab libraries are in
    - <matlab_dir>/bin/*
    So we should search bin/* for libraries.

    All information that are needed for searching should be supplied to the constructor
    of this class through variable "hints". This variable is a dictionary of signatures
    that can be used in searching.

    A typical signature dictionary looks like
    {
    "executable": "matlab",
    "c libraries": "bin/*",
    }
    """

    mechanism = "search paths of a package by looking for executables"

    scheme = {'root': '.',
              'c headers': 'include',
              'c libraries': 'lib',
              'python modules': 'python'}


    def _extract(self):
        """
        extract my paths by using infects/utils to search for paths using given signature

        signatures:      signature of the package. for example, the name of the executable.
        
        derivedFrom:    name of the package from which the paths of this package could be derived

        """
        signatures  = self._hintsToFindPaths
        derivedFrom = self._derivedFrom
        if not isinstance(signatures, dict):
            raise ValueError("expect a dictionary of signatures for finding a package") 
        self.signatures = signatures
        

        #for firendly output
        base_desc = self.description
        desc_format_str = 'path to %s directory of ' + base_desc

        #find out paths
        self.root = root = self.getRoot(desc_format_str, derivedFrom)
        include = self.getSubdirectory('c headers', desc_format_str)
        clib = self.getSubdirectory('c libraries', desc_format_str)
        python = self.getSubdirectory('python modules', desc_format_str)
                           
        from .Paths import Paths
        return Paths( self.name,
                      root = root,
                      includes=[include],
                      clibs=[clib],
                      modules=[python],
                      description = self.description,
                      origin = self.mechanism,)


    def getRoot(self, desc_format_str, derivedFrom):
        #
        desc = desc_format_str % " root"
        #
        print("Searching for %s using mechansim \"%s\", which is %s ..." % (
            self.name, self.mechanism, desc))
        executable = self.signatures['executable']
        res = get_usingExec( executable )
        print(" * found --> %s" % res)
        return res

    
    def getSubdirectory( self, type, desc_format_str ):
        desc = desc_format_str % type
        default = _getDefaultDir( self.root, self.scheme[type])
        signature = self.signatures.get(type)
        if not signature: return default
        else:
            print("Searching for %s of %s, which is %s ..." % (type, self.name, desc)) #, end=' ')
            pattern = self.signatures[type]
            res = findpackage( pattern, self.root, 1 )
            print("found --> %s" % res)
            return res
        raise            
    


  
def _getDefaultDir( packageDir, subDir ):
    import os
    if subDir: return os.path.join( packageDir, subDir )
    else : return None
