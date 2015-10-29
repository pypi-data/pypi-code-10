__doc__ = """search paths of a package at default locations"""
__author__ = "Jiao Lin"


from .PathsFinder import PathsFinder as base, ValidationError


class PathsFinder(base):

    """
    search paths of a package by looking at the default locations
    """

    mechanism = "search paths of a package by looking at default locations"

    scheme = {'root': '.',
              'c headers': 'include',
              'c libraries': 'lib',
              'python modules': 'python'}


    def _extract(self):
        """
        extract my paths by using infects/utils to search for paths using given signature

        signatures:      signature of the package. here, actually it is the paths to the default locations. if not supplied, it will be /usr, /usr/local etc for the linux system
        """
        signatures  = self._hintsToFindPaths
        if signatures is None:
            signatures = self._getDefaultLocations()
        if not isinstance(signatures, tuple):
            raise ValueError("expect a tuple of paths to default locations") 
        self.signatures = signatures

        #find out paths
        for location in signatures:
            paths = self._createPaths(location)
            try:
                self._validate(paths)
            except ValidationError:
                import traceback
                from ..logger import debug
                debug('failed to find %s in %s. traceback: %s' % (
                        self.name, location, traceback.format_exc())
                      )
            else:
                return paths
            continue
        raise RuntimeError("Cannot find %s in default locations %s" % (
            self.name, signatures))


    def _getDefaultLocations(self):
        # XXX: should implement windows case too
        return '/usr', '/usr/local'


    def _createPaths(self, root):
        include = self.getSubdirectory(root, 'c headers', )
        clib = self.getSubdirectory(root, 'c libraries', )
        python = self.getSubdirectory(root, 'python modules', )
                           
        return Paths( 
            self.name,
            root = root,
            includes=[include],
            clibs=[clib],
            modules=[python],
            description = self.description,
            origin = self.mechanism,)
    
    
    def getSubdirectory( self, root, type):
        return _getDefaultDir( root, self.scheme[type])
    

def _getDefaultDir( packageDir, subDir ):
    import os
    if subDir: return os.path.join( packageDir, subDir )
    else : return None


from .Paths import Paths

