# -*- coding: utf-8 -*-

"""Utilities for performing merges."""

from . import api


def prepare(data):
    """Restructure/prepare data about merges for output."""
    sha = data.get("sha")
    commit = data.get("commit")
    message = commit.get("message")
    tree = commit.get("tree")
    tree_sha = tree.get("sha")
    return {"message": message, "sha": sha, "tree": {"sha": tree_sha}}


def merge(profile, head, base, commit_message=None):
    """Merge the head of a branch into the base branch.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        head
            The head to merge. It can be a SHA, or a branch name.

        base
            The name of the branch to merge the specified head into.

        commit_message
            The message to give for the commit.

    Returns:
        A dict with data about the merge.

    """
    if not commit_message:
        commit_message = "Merged " + head + " into " + base + "."
    payload = {
        "base": base,
        "head": head,
        "commit_message": commit_message,
        }
    response = api.post_merge_request(profile, payload)
    data = None
    if response.status_code == 201:
        json_data = response.json()
        data = prepare(json_data)
    return data
