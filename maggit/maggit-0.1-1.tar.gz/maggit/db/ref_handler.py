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

import re
from maggit.io.packedref import packed_ref_parse
from binascii import unhexlify, hexlify

refheadparser = re.compile(r"ref: refs/heads/([a-zA-Z_.]+)")

class RefHandler:
    """The RefHandler manage the references in a repository.

    A RefHandler handle only the references. Not the git objects.
    """
    def __init__(self, gitdir):
        self.gitdir = gitdir
        self.packed_refs = {e[0].decode():e[1:] for e in packed_ref_parse(self.gitdir/'packed-refs')}

    @property
    def HEAD(self):
        """The current checkouted branch"""
        with (self.gitdir/'HEAD').open() as f:
            content = f.read()
        match = refheadparser.match(content)
        brancheName = match.group(1)
        return brancheName

    def _list_refs(self, subdir):
        refs = set()
        heads = self.gitdir/'refs'/subdir
        for name in heads.iterdir():
            refs.add(name.name)
        startText = 'refs/%s/'%subdir
        refs |= {e[len(startText):] for e in self.packed_refs if e.startswith(startText)}
        return refs

    @property
    def branches(self):
        """A iterator of branches in the repo"""
        yield from self._list_refs('heads')

    @property
    def tags(self):
        """A iterator of tags in the repo"""
        yield from self._list_refs('tags')

    def check_ref_exists(self, ref):
        """Check that a ref exist in the git bdd.

        Arguments:
            ref(str) : the ref to check.

        Returns:
            bool: True if the ref exists, else False
        """
        reffile = self.gitdir/'refs'/ref
        return reffile.exists()

    def get_ref_sha(self, ref):
        """Return the sha corresponding to the ref.

        Arguments:
            ref(str) : the ref to get.

        Returns:
            bytes: The sha corresponding to the ref
        """
        reffile = self.gitdir/'refs'/ref
        if reffile.exists():
            with reffile.open('br') as f:
                sha = unhexlify(f.read(40))
        else:
            sha = self.packed_refs['refs/'+ref][0]
        return sha

    def get_peel_ref_sha(self, ref):
        reffile = self.gitdir/'refs'/ref
        if reffile.exists():
            # if the loose ref file exist, we must not used peeled value.
            return None
        try:
            return self.packed_refs['refs/'+ref][1]
        except KeyError:
            return None
