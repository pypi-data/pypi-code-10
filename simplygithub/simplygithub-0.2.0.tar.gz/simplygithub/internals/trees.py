# -*- coding: utf-8 -*-

"""Utilities for getting/creating trees."""

from . import api


def prepare(data):
    """Restructure/prepare data about trees for output."""
    sha = data.get("sha")
    tree = data.get("tree")
    return {"sha": sha, "tree": tree}


def get_tree(profile, sha, recursive=True):
    """Fetch a tree.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        sha
            The SHA of the tree to fetch.

        recursive
            If ``True``, traverse all subtrees and their subtrees, all the
            way down. That will return a list of all objects in the tree,
            all levels deep.

    Returns:
        A dict with data about the tree.

    """
    resource = "/trees/" + sha
    if recursive:
        resource += "?recursive=1"
    data = api.get_request(profile, resource)
    return prepare(data)


def create_tree(profile, tree):
    """Create a new tree.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        tree
            A list of blob objects (each with a path, mode, type, and
            content or sha) to put in the tree.

    Returns:
        A dict with data about the tree.

    """
    resource = "/trees"
    payload = {"tree": tree}
    data = api.post_request(profile, resource, payload)
    return prepare(data)
