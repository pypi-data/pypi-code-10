# -*- coding: utf-8 -*-

"""Utilities for getting/creating commits."""

from . import api


def prepare(data):
    """Restructure/prepare data about commits for output."""
    message = data.get("message")
    sha = data.get("sha")
    tree = data.get("tree")
    tree_sha = tree.get("sha")
    return {"message": message, "sha": sha, "tree": {"sha": tree_sha}}


def get_commit(profile, sha):
    """Fetch a commit.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        sha
            The SHA of the commit to fetch.

    Returns:
        A dict with data about the commit.

    """
    resource = "/commits/" + sha
    data = api.get_request(profile, resource)
    return prepare(data)


def create_commit(profile, message, tree, parents):
    """Create a commit.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        message
            The commit message to give to the commit.

        tree
            The SHA of the tree to assign to the commit.

        parents
            A list enumerating the SHAs of the new commit's parent commits.

    Returns:
        A dict with data about the commit.

    """
    resource = "/commits"
    payload = {"message": message, "tree": tree, "parents": parents}
    data = api.post_request(profile, resource, payload)
    return prepare(data)
