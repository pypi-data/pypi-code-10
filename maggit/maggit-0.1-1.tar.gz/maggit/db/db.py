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

from pathlib import Path
import hashlib

from maggit.io import loose, pack
from maggit.const import ObjectType
from binascii import unhexlify, hexlify

class Gitdb:
    """The Gitdb, unify all loose/pack io function to provide a coherent access
    to content of a git repository.

    A Gitdb handle only the reading of git objects. Not the references, remotes, ...

    Arguments:
        rootdir(path): The path of the objects directory (.git/objects)
    """
    def __init__(self, rootdir):
        self.rootdir = Path(rootdir)
        self.gen_pack_list()

    def _get_pathfile(self, sha):
        sha = hexlify(sha).decode()
        return self.rootdir.joinpath(sha[:2], sha[2:])

    def gen_pack_list(self):
        self.packs = {}
        self.pack_dir = self.rootdir.joinpath("pack")
        packs = self.pack_dir.glob('*.idx')
        for p in packs:
            packName = str(p)[:-4]
            p_pack = packName+".pack"
            if not (self.pack_dir/p_pack).exists():
                print(p_pack, "not exists")
                continue
            packIndex = pack.GitPackIndex(self.pack_dir/(packName+'.idx'))
            self.packs[packName] = (packIndex, None)

    def get_pack(self, sha):
        """Get a pack containing the sha

        Arguments:
            sha : The sha of the object

        Returns:
            The :class:`~maggit.io.pack.GitPack` containing the sha
        """
        for packName, index_data in self.packs.items():
            p_pack = packName + ".pack"
            packIndex, packData = index_data

            try:
                offset = packIndex.get_offset(sha)
            except KeyError:
                # Not in this pack
                continue
            else:
                if packData is None:
                    packData = pack.GitPack(self.pack_dir/p_pack, packIndex)
                    self.packs[packName] = packIndex, packData
                return packIndex, packData, offset

    def object_exists(self, sha):
        """Return True if the sha exists in the db"""
        pathfile = self._get_pathfile(sha)
        if pathfile.exists():
            return True
        index_pack = self.get_pack(sha)
        if index_pack:
            return True
        return False

    def get_full_sha(self, prefix):
        """Return the full Sha of the prefix

        Arguments:
            prefix(bytes): The beginning of a sha.

        Returns:
            The corresponding (bytes).

        Exemples:
            >>> repo.get_full_sha(b'bf09f0a9')
            <Sha b'bf09f0a9...'>

        Raises:
            :Exception: If number of object corresponding to prefix is not equal to one.
        """
        for _, index_data in self.packs.items():
            # be sure that a .pack exits
            packIndex, _ = index_data
            try:
                return packIndex.get_full_sha(prefix)
            except KeyError:
                # Not in this pack
                continue

        # Look in loose objects
        directory = self.rootdir.joinpath(prefix[:2])
        if not directory.exists():
            raise KeyError
        entries = directory.glob(prefix[2:]+'*')
        try:
            entry = next(entries)
        except StopIteration:
            # len(entries) < 1
            raise KeyError
        try:
            _ = next(entries)
            # len(entries) > 1
            raise KeyError
        except StopIteration:
            pass
        return unhexlify((prefix[:2] + str(entry.name)).encode('utf8'))

    def object_content(self, sha):
        pathfile = self._get_pathfile(sha)
        if pathfile.exists():
            return loose.object_content(pathfile)
        index_pack = self.get_pack(sha)
        try:
            _, pack, offset = index_pack
        except TypeError:
            raise KeyError
        return pack.read_object(offset)

    def object_type(self, sha):
        """Return the type of the object associated to sha.

        Arguments:
            sha: The sha of the object.

        Returns:
            The type of the object.
        """
        return self.object_content(sha)[0]

    def _object_write(self, sha, content):
        if self.object_exists(sha):
            return
        pathfile = self._get_pathfile(sha)
        loose.object_write(pathfile, content)

    def blob_content(self, sha):
        """Read and parse a object assuming it is a blob.

        Arguments:
            sha : The sha of the object.

        Returns:
            The content of the blob (bytes).

        Raises:
            ValueError: If the object is not a blob.
        """
        type_, content = self.object_content(sha)
        if type_ != ObjectType.blob:
            raise ValueError("Object %s is of type %s (not blob)"%(sha, type_))
        return content

    def blob_write(self, content):
        raw, sha = loose.object_rawsha(ObjectType.blob, content)
        self._object_write(sha, raw)
        return sha

    def tree_content(self, sha):
        """Read and parse a object assuming it is a tree.

        Arguments:
            sha : The sha of the object.

        Returns:
            List[Tuple[bytes, Tuple[bytes, bytes]]]:

            A list of (path, (mode, sha)) where :

             - path is the name of the entry.
             - mode is the git mode.
             - sha is the sha of the blob/tree object.

        Raises:
            ValueError: If the object is not a tree.
        """
        type_, content = self.object_content(sha)
        if type_ != ObjectType.tree:
            raise ValueError("Object %s is of type %s (not tree)"%(sha, type_))
        return loose.tree_parse(content)

    def tree_write(self, entries):
        raw, sha = loose.object_rawsha(ObjectType.tree, loose.tree_gen(entries))
        self._object_write(sha, raw)
        return sha

    def commit_content(self, sha):
        """Read and parse a object assuming it is a commit.

        Arguments:
            sha : The sha of the object.

        Returns:
            bytes, list[bytes], bytes, bytes, bytes:

            A tuple (tree, parents, message, author, committer) where:

             - tree is the sha of the tree object of the commit(unhexlified bytes).
             - parents is a list of sha of the parents commit.
             - message is the message of the commit.
             - author is the name (b'name <email> timestamp') of the author.
             - author is the name (b'name <email> timestamp') of the committer.

        Raises:
            ValueError: If the object is not a commit.
        """
        type_, content = self.object_content(sha)
        if type_ != ObjectType.commit:
            raise ValueError("Object %s is of type %s (not commit)"%(sha, type_))
        return loose.commit_parse(content)

    def commit_write(self, treesha, message, author, authorDate, committer, committerDate, parents=[]):
        raw, sha = loose.object_rawsha(ObjectType.commit, loose.commit_gen(treesha, message, author, authorDate, committer, committerDate, parents))
        self._object_write(sha, raw)
        return sha

    def tag_content(self, sha):
        """Read and parse a object assuming it is a tag.

        Arguments:
            sha : The sha of the object.

        Returns:
            bytes, bytes, bytes, bytes, bytes:

            A tuple (object, objecttype, tag, tagger, message) where:

             - object is the sha of the tagged object (unhexlified bytes).
             - objecttype is the type of the tagged object.
             - tag is the name of the tag.
             - tagger is the name (b'name <email> timestamp') of the tagger.
             - message is the message of the tag.

        Raises:
            ValueError: If the object is not a tag.
        """
        type_, content = self.object_content(sha)
        if type_ != ObjectType.tag:
            raise ValueError("Object %s is of type %s (not, tag)"%(sha, type_))
        return loose.tag_parse(content)

    def tag_write(self, objectsha, tag, tagger, tagDate, message):
        objecttype = self.object_type(objectsha)
        raw, sha = loose.object_rawsha(ObjectType.tag, loose.tag_gen(objectsha, objecttype, tag, tagger, tagDate, message))
        self._object_write(sha, raw)
        return sha
