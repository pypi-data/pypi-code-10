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

from . import git_objects
from . import refs
from .const import ObjectType
from .sha import Sha
import os
from pathlib import Path

from maggit import db

class Repo(db.Repo):
    """This is the central piece of a git repository.
    """
    @property
    def HEAD(self):
        """The current checkouted branch"""
        return refs.Branche(self, db.Repo.HEAD.__get__(self))

    @property
    def branches(self):
        """A dict of branches in the repo"""
        return {k:refs.Branche(self, k) for k in db.Repo.branches.__get__(self)}

    @property
    def tags(self):
        """A dict of tags in the repo"""
        return {k:refs.Tag(self, k) for k in db.Repo.tags.__get__(self)}

    def get_object(self, sha, type_=None):
        """Get a git object for the sha.

        Arguments:
            sha(:class:`~maggit.Sha`) : The sha of the object.
            type_(:class:`~maggit.ObjectType` or None) :
                The type of the object.
                If this is None (or not set), the type is detected automatically.

        Returns:
             A :class:`~maggit.git_objects.GitObject` object for this sha.

        Raises:
             :Exception: If sha doesn't name a object.
        """
        type_ = type_ or self.db.object_type(sha)
        return {ObjectType.blob   : lambda: git_objects.Blob(self, sha),
         ObjectType.commit : lambda: Commit(self, sha),
         ObjectType.tree   : lambda: git_objects.Tree(self, sha),
         ObjectType.tag    : lambda: git_objects.Tag(self, sha)
        }[type_]()

    def get_tag(self, sha):
        """Get a tag object for the sha.

        Arguments:
            sha(:class:`~maggit.Sha`) : The sha of the tag.

        Returns:
             A :class:`~maggit.git_objects.Tag` object for this sha.

        Raises:
             :Exception: If sha doesn't name a tag object.
        """
        return git_objects.Tag(self, sha)

    def get_commit(self, sha):
        """Get a commit object for the sha.

        Arguments:
            sha(:class:`~maggit.Sha`) : The sha of the commit.

        Returns:
             A :class:`~maggit.repo.Commit` object for this sha.

        Raises:
             :Exception: If sha doesn't name a commit object.
        """
        return Commit(self, sha)

    def get_tree(self, sha):
        """Get a tree object for the sha.

        Arguments:
            sha(:class:`~maggit.Sha`) : The sha of the tree.

        Returns:
             A :class:`~maggit.git_objects.Tree` object for this sha.

        Raises:
             :Exception: If sha doesn't name a tree object.
        """
        return git_objects.Tree(self, sha)

    def get_blob(self, sha):
        """Get a blob object for the sha.

        Arguments:
            sha(:class:`~maggit.Sha`) : The sha of the blob.

        Returns:
             A :class:`~maggit.git_objects.Blob` object for this sha.

        Raises:
             :Exception: If sha doesn't name a blob object.
        """
        return git_objects.Blob(self, sha)

    def get_full_sha(self, prefix):
        """Return the full Sha of the prefix

        Arguments:
            prefix(bytes): The beginning of a sha.

        Returns:
            The :class:`~maggit.Sha` corresponding.

        Exemples:
            >>> repo.get_full_sha(b'bf09f0a9')
            <Sha b'bf09f0a9...'>

        Raises:
            :Exception: If number of object corresponding to prefix is not equal to one.
        """
        sha = db.Repo.get_full_sha(self, prefix)
        return Sha(sha)

    def get_ref_sha(self, name):
        """Return the Sha corresponding to the reference name

        Arguments:
            name(str): The reference name.

        Returns:
            The :class:`~maggit.Sha` corresponding.

        Exemples:
            >>> repo.get_ref_sha('master')
            <Sha >

        Raises:
            :Exception: If number of object corresponding to prefix is not equal to one.
        """
        sha = db.Repo.get_ref_sha(self, name)
        return Sha(sha)


class Entry:
    """A Entry represent a entry (file or directory) at a specific time.

    We can somehow see a repository as a complex 2 dimentionnal array.
    Commits (and so the history) are rows.
    Files (and Trees) are columns.

    In this situations, Entry are the cells of this array.
    """
    def __init__(self, repo, commit, path, mode, gitObject):
        self.repo = repo #:The repo associated to the Entry
        self.commit = commit
        self.path = path
        self.mode = mode
        self.gitObject = gitObject

    @property
    def parents(self):
        """The previous versions of the files.

        Previous versions can be equal to the current one if the current commit
        introduce no change on this file.

        The length of the parents will most of the time be 1 but may be greater
        in case of merge.
        """
        return (p.get_file(self.path) for p in self.commit.parents)

    def get_first_appearance(self):
        """Get the commit who firstly introduce the current version of the change.

        Returns:
            A :class:`~maggit.repo.Commit`
        """
        return self.commit.get_first_appearance(self.path)


class Commit(git_objects.Commit):
    def get_file(self, path):
        """Get an entry corresponding to the path in the commit

        Arguments:
            path(str or Path) : The path of the file to look at.

        Returns:
            A :class:`~maggit.repo.Entry` corresponding.

        Raise:
            KeyError if the path is not existing.
        """
        path = Path(path)
        current = self.tree
        for part in path.parts:
            mode, current = current[part]
        return Entry(self.repo, self, path, mode, current)

    def get_first_appearance(self, path):
        """Return the commit where the present version of path was introduce.

        Arguments:
            path(str or path): The path of the file.

        Returns:
            A :class:`maggit.repo.Commit`

        Exemples:
            >>> first_appearance_commit = this_commit.get_first_appearance(path)
            >>> # first_appearance_commit is the first one, so previous version differs
            >>> parent = first_appearance_commit.parents[0]
            >>> assert first_appearance_commit.get_file(path).gitObject != parent.get_file(path).gitObject
            >>> # from this_commit to first_appearance_commit, there is no change
            >>> current = this_commit
            >>> while current != first_appearance_commit:
            ...     assert current.get_file(path).gitObject == this_commit.get_file(path).gitObject
            ...     current = current.parents[0]
        """

        current = self
        while True:
            try:
                parent = current.parents[0]
            except IndexError:
                # No parent
                return None

            c_tree = current.tree
            p_tree = parent.tree
            if c_tree.is_entry_diff(p_tree, path):
                # There is a diff, current is the commit who introduce
                # this versions.
                return current
            # No diff for this path
            # Continue check in the history
            current = parent

    def get_first_appearances(self, root=None, depthLimit=None):
        """Return the first appearances for all entry in root.

        This is mostly equivalent to `{path:commit.get_first_appearance(path) for path in commit.tree.entries}`
        (if root is None).
        But a way more performant as diving into history is made once.

        Arguments:
            root(str or Path): In wich subdirectory we must look.
            depthLimit(int)  : The commit limit number we go in history
                               If depthLimit is specified, and for a entry the first appearance is older than depthLimit,
                               the entry will be present in the dictionnary with a None value.

        Returns:
            A dict of (Path, :class:`maggit.repo.Commit`).
        """
        entries_left = set(self.tree.entries.keys())
        root = Path(root or "").parts
        result = {}
        current = self
        c_trees = [current.tree]
        for r in root:
            c_trees.append(c_trees[-1][r])
        depth = 0
        while entries_left:
            depth = depth + 1
            if depthLimit and depth>depthLimit:
                result.update({e:None for e in entries_left})
                break
            try:
                parent = current.parents[0]
            except IndexError:
                # No parent
                result.update({e:current for e in entries_left})
                break

            if parent._tree == c_trees[0]._sha:
                # Tree is equal, advance in history
                current = parent
                # No need to change c_trees to p_trees, they are equals
                continue

            p_trees = [parent.tree]
            need_continue = False
            for i, r in enumerate(root, 1):
                p_trees.append(p_trees[-1][r])
                if p_trees[-1] == c_trees[i]:
                    current = parent
                    c_trees[:i] = p_trees
                    need_continue = True
                    break
            if need_continue:
                continue

            # Ok, now we've got two trees where some entries differ
            # Do the job
            _, diff, in_current, _ = c_trees[-1].gen_entries_diff(p_trees[-1], entries_left)
            diff |= in_current
            result.update({e:current for e in diff&entries_left})
            entries_left -= diff

            current = parent
            c_trees = p_trees

        return result
