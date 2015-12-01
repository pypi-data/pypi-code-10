import git as _git
import os as _os
import re as _re
import importlib as _importlib


class CheckMod(object):
    def __init__(self, mod):
        self._mod = mod
        self._version = None

        # Get main module
        res = _re.search('.*(?=\.)', '{}.'.format(self.mod.__name__))
        self._mainmod = _importlib.import_module(res.group())

        # Get main module path
        self._mainmod_path = _os.path.dirname(
            _os.path.dirname(self.mainmod.__file__)
        )

        # Get repo
        self._repo = _git.Repo(self.mainmod_path)

        # Get hexsha
        self._hexsha = self._repo.head.object.hexsha

    @property
    def mod(self):
        return self._mod

    @property
    def mainmod(self):
        return self._mainmod

    @property
    def mainmod_path(self):
        return self._mainmod_path

    @property
    def repo(self):
        return self._repo

    @property
    def hexsha(self):
        return self._hexsha

    @property
    def version(self):
        for tag in self.repo.tags:
            if tag.object.hexsha == self.hexsha:
                self._version = tag.name

        return self._version
