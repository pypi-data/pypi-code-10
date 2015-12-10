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

_setattr = object.__setattr__
from .sha import Sha
from .const import ObjectType
import collections

__all__ = ['Blob', 'Tree', 'Commit', 'Tag']

class GitObject:
    """The base class for all git objects.

    Git objects are conceptualy constant. However as we try to be lazy,
    slots are not fill at object creation and set when user read it.
    So GitObject are not constant but behave as if they were.


    Attributes:
        repo (:class:`~maggit.Repo`)               : The repo associated with the object.
        sha (:class:`~maggit.Sha`)                 : The sha of the object.
        gitType(:class:`~maggit.const.ObjectType`) : The type of the object.
    """

    __slots__ = ('repo',
                 'sha', '_sha')

    def _compute_sha(self):
        return Sha(self._sha)

    def __init__(self, repo, sha):
        _setattr(self, 'repo', repo)
        _setattr(self, '_sha', sha)

    def __getattr__(self, name):
        """This is call cause an attribute has not been found.
           This is probably cause the slot's descriptor raise a AttributeError.
           This means that we still not have read and parse the git object."""
        for c in type(self).__mro__:
            if name in getattr(c, '__slots__', []):
                break
        else:
            # Someone try to get a attribute that really not exists
            raise AttributeError("%r doesn's exist in %r"%(name, self))
        if hasattr(self, "_compute_"+name):
            f = getattr(self, "_compute_"+name)
            v = f()
            _setattr(self, name, v)
            return v
        self._read()
        # Now that _read update the attributes, try to look again
        return getattr(self, name)

    @staticmethod
    def __setattr__(name, value):
        raise RuntimeError("Cannot modify a GitObject")

    def __eq__(self, other):
        return self._sha == other._sha


class Blob(GitObject):
    """ A blob object.

    Attributes:
        content(bytes)      : This is the content of the blob.
    """
    __slots__ = ('content',)

    gitType = ObjectType.blob

    def _read(self):
        _setattr(self, 'content', self.repo.db.blob_content(self._sha))


class TreeDict(collections.Mapping):
    def __init__(self, repo, raw_mapping):
        self.repo = repo
        self.mapping = raw_mapping

    def __getitem__(self, name):
        mode_sha, obj  = self.mapping[name]
        if obj:
            return mode_sha[0], obj

        obj = self._create_object(*mode_sha)
        self.mapping[name] = (mode_sha, obj)
        return mode_sha[0], obj

    def __len__(self):
        return len(self.mapping)

    def __iter__(self):
        return iter(self.mapping)

    def get_sha(self, name):
        mode_sha, _  = self.mapping[name]
        return mode_sha[1]

    def _create_object(self, mode, _sha):
        if mode ==  b"40000":
            return self.repo.get_tree(_sha)
        else:
            return self.repo.get_blob(_sha)


class Tree(GitObject):
    """ A blob object.

    Attributes:
        entries(unmutable mapping) : This is the entries of the tree.
    """
    __slots__ = ('entries',)

    gitType = ObjectType.tree

    def _read(self):
        _entries = self.repo.db.tree_content(self._sha)
        _setattr(self, 'entries', TreeDict(self.repo, {e[0].decode('utf8'):(e[1], None) for e in _entries}))

    def __getitem__(self, name):
        """Return the entry corresponding  to the name"""
        return self.entries[name]

    def is_entry_diff(self, other, path):
        """Check if path is in both trees and if the two subfiles/subtrees differ

        Arguments:
            other(Tree): The other tree objet to compare from
            path(Path) : The path to check

        Returns:
            - False if there is no diff
            - True if the path is in both tree, but content differs
            - The tree that content the path if the path is in only one tree
        """
        sentries = self.entries
        oentries = other.entries
        for p in path.parts:
            try:
                sentries = sentries[p][1]
            except KeyError:
                # self doesn't contain the path
                return other
            try:
                oentries = oentries[p][1]
            except KeyError:
                # other doesn't contain the path
                return self
            if sentries == oentries:
                # Either entre or parent subtree is equal
                # Thanks to git hash we know that the final path will
                # be equal
                return False
        # We reach the end of the path and entries are differents
        return True

    def gen_entries_diff(self, other, subset=None):
        """Compare the twe tree and return four sets:

            - equal   : the entries that are in both self and other and are equal is both
            - diff    : the entries that are in both self and other but are not equal
            - in_self : the entries that are only in self
            - in_other : the entries that are only in other
        """
        result = {}
        sentries = self.entries.keys()
        oentries = other.entries.keys()
        if subset is not None:
            sentries &= subset
            oentries &= subset

        in_both   = sentries & oentries
        only_in_s = sentries - in_both
        only_in_o = oentries - in_both
        equal     = set(k for k in in_both if self.entries.get_sha(k)==other.entries.get_sha(k))
        diff      = in_both - equal

        return equal, diff, only_in_s, only_in_o

    def gen_diff_map(self, other):
        equal, diff, in_self, in_other = self.gen_entries_diff(other)

        result =     { k:'=' for k in equal}
        result.update((k,'!') for k in diff)
        result.update((k,'<') for k in in_self)
        result.update((k,'>') for k in in_other)

        return result

    def gen_full_diff_map(self, other):
        _, diff, in_self, in_other = self.gen_entries_diff(other)
        result = {}

        for d in diff:
            sentry = self.entries[d][1]
            oentry = other.entries[d][1]
            if sentry.gitType == ObjectType.tree and oentry.gitType == ObjectType.tree:
                sub_diff = sentry.gen_full_diff_map(oentry)
                result.update(("%s/%s"%(d, e),sd) for e, sd in sub_diff.items())
            elif sentry.gitType == ObjectType.blob and oentry.gitType == ObjectType.blob:
                result[d] = '!'

        for n in in_self:
            sentry = self.entries[n][1]
            if sentry.gitType == ObjectType.tree:
                sub_new = sentry.list_all_files()
                result.update(("%s/%s"%(n, e),'<') for e in sub_new)
            else:
                result[n] = '<'

        for o in in_other:
            oentry = other.entries[d][1]
            if oentry.gitType == ObjectType.tree:
                sub_old = oentry.list_all_files()
                result.update(("%s/%s"%(o, e),'>') for e in sub_old)
            else:
                result[o] = '>'

        return result

    def list_all_files(self):
        result = []
        for e in self.entries:
            if self.entries[e].gitType == ObjectType.tree:
                result.extend("%s/%s"%(e, i) for i in self.entries[e].list_all_files())
            else:
                result.append(e)
        return result

class Commit(GitObject):
    """ A commit object.

    Attributes:
        tree(:class:`maggit.git_objects.Tree`)          : The tree object associated with the commit.
        parents(tuple)      : The parents of the commits.
                              Most of the time, there will only one parent.
                              In case of branch merge, there will be more than one parent.
        author(bytes)       : The author of the commit.
                              (This is the raw content in the commit.
                              This means that it is a bytes with the name, email and commit timestamp)
        committer(bytes)    : The committer of the commit.
                              (This is the raw content in the commit.
                              This means that it is a bytes with the name, email and commit timestamp)
        first_line(str)     : The first line of the commit message.
        message(str)        : The full commit message (including the first line).
    """
    __slots__ = ('tree', '_tree',
                 'parents', '_parents',
                 'author', 'committer',
                 'first_line', 'message', '_messageLines')

    gitType = ObjectType.commit

    def _compute_tree(self):
        return self.repo.get_tree(self._tree)

    def _compute_parents(self):
        return tuple(self.repo.get_commit(p) for p in self._parents)

    def _compute_first_line(self):
         return self._messageLines[0].decode('utf8')

    def _compute_message(self):
        return b'\n'.join(self._messageLines).decode('utf8')

    def _read(self):
        (treesha, parents, messageLines, author, committer) = self.repo.db.commit_content(self._sha)
        _setattr(self, '_tree', treesha)
        _setattr(self, '_parents', parents)
        _setattr(self, '_messageLines', messageLines)
        _setattr(self, 'author', author)
        _setattr(self, 'committer', committer)


class Tag(GitObject):
    """ A tag object.

    Attributes:
        object(:class:`GitObject`)      : The git object tagged by this tag.
        objectType(:class:`~maggit.const.ObjectType`) : The type of the git object tagged by this tag.
        tag(str)               : The name of the tag.
        tagger(bytes)          : The person who create the tag.
                                 (This is the raw content in the tag.
                                 This means that it is a bytes with the name, email and tag timestamp)
        first_line(str)        : The first line of the tag message.
        message(str)           : The full tag message (including the first line).
    """
    __slots__ = ('object', '_object',
                 'objectType', '_objectType',
                 'tag',
                 'tagger',
                 'first_line', 'message', '_messageLines')

    gitType = ObjectType.tag

    def _compute_object(self):
        return self.repo.get_object(self._object, self.objectType)

    def _compute_objectType(self):
        return ObjectType(self._objectType)

    def _compute_first_line(self):
         return self._messageLines[0].decode('utf8')

    def _compute_message(self):
        return b'\n'.join(self._messageLines).decode('utf8')

    def _read(self):
        (_object, objtype, tag, tagger, messageLines) = self.repo.db.tag_content(self._sha)
        _setattr(self, '_object', _object)
        _setattr(self, '_objectType', objtype)
        _setattr(self, 'tag', tag)
        _setattr(self, 'tagger', tagger)
        _setattr(self, '_messageLines', messageLines)
