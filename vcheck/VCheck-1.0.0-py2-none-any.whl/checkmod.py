import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import git as _git

import os as _os
import re as _re
import importlib as _importlib
from .versionerror import VersionError as _VersionError


class CheckMod(object):
    """A class containing the main information on a module for version checking.

    """
    def __init__(self, mod):
        self._mod = mod
        self._version = None

        # Get main module
        res = _re.search('.*?(?=\.)', '{}.'.format(self.mod.__name__))
        self._mainmod = _importlib.import_module(res.group())

        # Get main module path
        self._mainmod_path = _os.path.dirname(self.mainmod.__file__)

        if self.repo.is_dirty():
            raise _VersionError('Repo for module {} is dirty (changes have been made); version not well-defined.'.format(self.mainmod.__name__))

    def vcheck(self, hexsha=None, version=None):
        """
        vchecky(hexsha, version)

        Checks to see if the module matches the version requested.

        Parameters
        ----------
        hexsha : str
            A git sha1 signature indicating a particular commit.
        version : str
            A string indicating a particular git tag.

        Raises
        ------
        vcheck.VersionError
            If there has been an error identifying the module version.
        """
        if hexsha is not None and version is not None:
            raise ValueError('Only specify either hexsha ({}) or version({})'.format(hexsha, version))
        elif hexsha is None and version is None:
            raise ValueError('Neither hexsha nor version specified')
        elif hexsha is not None:
            if self.repo.head.object.hexsha == hexsha:
                return True
            else:
                return False
        elif version is not None:
    
            for _tag in self.repo.tags:
                if self.hexsha == _tag.object.hexsha:
                    if version == _tag.name:
                        return True
    
            raise _VersionError('Repo for module {} does not match a released version.'.format(self.mainmod.__name__))

    @property
    def mod(self):
        """
        The module being checked.
        """
        return self._mod

    @property
    def mainmod(self):
        """
        The root module being checked.
        """
        return self._mainmod

    @property
    def mainmod_path(self):
        """
        The path to the root module being checked.
        """
        return self._mainmod_path

    @property
    def repo(self):
        """
        Object representing the git repo of the main module.
        """
        self._repo = _git.Repo(_os.path.dirname(self.mainmod_path))
        return self._repo

    @property
    def hexsha(self):
        """
        The hex sha1 of the git repo of the main module.
        """
        self._hexsha = self.repo.head.object.hexsha
        return self._hexsha

    @property
    def version(self):
        """
        The version of the main module.
        """

        try:
            self._version = None
            for tag in self.repo.tags:
                if tag.object.hexsha == self.hexsha:
                    self._version = tag.name
        except:
            raise _VersionError('The module is not in a git repository.')

        if self._version is None:
            raise _VersionError('The module has no version property.')
        return self._version
