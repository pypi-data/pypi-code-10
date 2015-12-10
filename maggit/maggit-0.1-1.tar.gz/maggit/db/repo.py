# This file is part of maggit.
#
# Copyright 2015 Matthieu Gautier <dev@mgautier.fr>
#
# Pit is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# Additional permission under the GNU Affero GPL version 3 section 7:
#
# If you modify this Program, or any covered work, by linking or
# combining it with other code, such other code is not for that reason
# alone subject to any of the requirements of the GNU Affero GPL
# version 3.
#
# You should have received a copy of the GNU Affero General Public License
# along with maggit.  If not, see http://www.gnu.org/licenses
#
# In summary:
# - You can use this program for no cost.
# - You can use this program for both personal and commercial reasons.
# - You do not have to share your own program's code which uses this program.
# - You have to share modifications (e.g bug-fixes, improvements) you've made to this program.

from .db import Gitdb
import os
from pathlib import Path
from .ref_handler import RefHandler

default_config = '''[core]
    repositoryformatversion = 0
    filemode = true
    bare = {bare}
    logallrefupdates = true
'''

git_init_file = {
    'HEAD': "ref: refs/heads/master",
    'description': "Unnamed repository; edit this file 'description' to "
        "name the repository.\n",
    'config': default_config,
}


class Repo(RefHandler):
    """This is the low level Repository class.

    The repo make the link between all other low level subsystems and
    recreate a coherent database.

    Arguments:
        gitdir(path): The directory path of the repository,

                      If is None, the current working directory is assumed.
        disable_directoryLooking(bool): If True, assume that the gitdir is a
                                        valid path so do not search for a valid
                                        git repository in parents and gitdir must
                                        not be None.

        bare(bool): Does the repository is a bare one. Only relevant if
                    disable_directoryLooking is True. Else, the bare attribute is
                    detected from the git repository structure.
    """
    def __init__(self, gitdir=None, disable_directoryLooking=False, bare=False):
        self.bare = bare
        if disable_directoryLooking:
            gitdir = Path(gitdir)
            if not self._check_is_git_dir(self.gitdir):
                raise Exception("%r is not a valid git directory", gitdir)
        else:
            self.bare, gitdir = self.get_git_dir(gitdir)

        # Initialise the refdb
        RefHandler.__init__(self, gitdir)
        object_dir = self._get_object_dir()
        self.db = Gitdb(object_dir)

    @classmethod
    def init_repo(cls, gitdir, bare=False):
        """Instantiate a new git repo at the given location."""
        gitdirpath = Path(gitdir)

        if not bare:
            gitdirpath = gitdirpath/'.git'

        for folder in [
                'branches', 'hooks',
                Path('info')/'excludes',
                Path('objects')/'info',
                Path('objects')/'pack',
                Path('refs')/'heads',
                Path('refs')/'tags',
                ]:
            nfolder = gitdirpath/folder
            try:
                nfolder.mkdir(parents=True)
            except FileExistsError:
                pass

        for filename, content in git_init_file.items():
            nfile = gitdirpath/filename
            try:
                with nfile.open('x') as stream:
                    stream.write(content.format(bare="true" if bare else "false"))
            except FileExistsError:
                pass

        return cls(gitdir)

    @staticmethod
    def _check_is_git_dir(path):
        return ( path.joinpath('HEAD').is_file()
             and path.joinpath('config').is_file()
             and path.joinpath('refs').is_dir()
             and path.joinpath('objects').is_dir())

    @classmethod
    def get_git_dir(cls, dirToCheck=None):
        # [TODO] We probably need to read the config
        # instead of supposing from directories structure.
        git_dir = os.environ.get('GIT_DIR', None)
        if git_dir:
            if cls._check_is_git_dir(git_dir):
                raise Exception("$GIT_DIR (%s) is not a valid git directory"%gitdir)
            return False, Path(git_dir)

        # Should we use Path.resolve here ?
        if dirToCheck is None:
            dirToCheck = os.getcwd()
        currentDir = Path(dirToCheck)
        while True:
            gitdir = currentDir/'.git'
            if gitdir.is_file():
                with gitdir.open("br") as f:
                     gitdir = Path(f.read().strip())
            if cls._check_is_git_dir(gitdir):
                return False, gitdir

            if cls._check_is_git_dir(currentDir):
                return True, currentDir

            parent = currentDir.parent
            if parent == currentDir:
                # We are at top
                raise Exception("No a git repository")
            currentDir = parent

    def _get_object_dir(self):
        object_dir = os.environ.get('GIT_OBJECT_DIRECTORY', None)
        if object_dir:
            return Path(object_dir)

        return self.gitdir/'objects'

    def get_full_sha(self, value):
        """Return the full sha of the value"""
        return self.db.get_full_sha(value)

