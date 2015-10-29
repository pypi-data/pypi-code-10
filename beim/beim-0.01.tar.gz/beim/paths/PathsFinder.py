__doc__ = """
The machinery to find paths of a package.
This module contains the base class.
"""

class PathsFinder:

    mechanism = "Warning: subclass should provide description of the mechanism used to determine the paths of a package"

    def __init__(self, name, description, hints = None, derivedFrom = None, validator=None):
        """PathsFinder(name, description, hints, derivedFrom) -> an instance of paths finder.
        This paths finder can find paths of a package with given name and description.
        The "hints" provided will be used to search or guess the paths.
        The paths could be derived from other package paths instance. If so, use keyword
          "derivedFrom"
        A function "validator" can be supplied to check whether the paths found is really valid
        """
        self.name = name
        self.description = description
        self._hintsToFindPaths = hints
        self._derivedFrom = derivedFrom
        self._validator = validator
        return

    def extract(self):
        '''extract my paths
        '''
        paths = self._extract()
        self._validate(paths)
        return paths


    def getPaths(self, name):
        from .Paths import Paths
        return Paths(name)


    def _extract(self):
        raise NotImplementedError("%s must override _extract" % self.__class__.__name__)


    def _validate(self, paths):
        validator = self._validator
        if validator:
            try:
                validator(paths)
            except Exception as e:
                raise ValidationError(str(e))
        return 
    



class ValidationError(Exception): pass


def exists(file, paths):
    'check if the given file exists in one of the given paths'
    import os, glob
    for path in paths:
        p = os.path.join(path, file)
        if glob.glob(p): return True
        continue
    return False


def assertExists(file, paths):
    if not exists(file, paths):
        raise RuntimeError('Failed to find %s in %s' % (file, paths))


