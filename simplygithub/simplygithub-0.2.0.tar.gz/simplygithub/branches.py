# -*- coding: utf-8 -*-

"""Utilities for getting/creating/listing branches."""

from .internals import (merges, refs)


def get_branch_sha(profile, name):
    """Get the SHA a branch's HEAD points to.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        name
            The name of the branch.

    Returns:
        The requested SHA.

    """
    ref = "heads/" + name
    data = refs.get_ref(profile, ref)
    head = data.get("head")
    sha = head.get("sha")
    return sha


def list_branches(profile):
    """List all branches.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

    Returns:
        A list of objects containing info about each branch.

    """
    data = refs.list_refs(profile, ref_type="heads")
    return data


def get_branch(profile, name):
    """Fetch a branch.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        name
            The name of the branch to fetch.

    Returns:
        A dict with data baout the branch.

    """
    ref = "heads/" + name
    data = refs.get_ref(profile, ref)
    return data


def create_branch(profile, name, branch_off):
    """Create a branch.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        name
            The name of the new branch.

        branch_off
            The name of a branch to create the new branch off of.

    Returns:
        A dict with data about the new branch.

    """
    branch_off_sha = get_branch_sha(profile, branch_off)
    ref = "heads/" + name
    data = refs.create_ref(profile, ref, branch_off_sha)
    return data


def update_branch(profile, name, sha):
    """Move a branch's HEAD to a new SHA.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        name
            The name of the branch to update.

        sha
            The commit SHA to point the branch's HEAD to.

    Returns:
        A dict with data about the branch.

    """
    ref = "heads/" + name
    data = refs.update_ref(profile, ref, sha)
    return data


def delete_branch(profile, name):
    """Delete a branch.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        name
            The name of the branch to delete.

    Returns:
        The response of the DELETE request.

    """
    ref = "heads/" + name
    data = refs.delete_ref(profile, ref)
    return data


def merge(profile, branch, merge_into):
    """Merge a branch into another branch.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        branch
            The name of the branch to merge.

        merge_into
            The name of the branch you want to merge into.

    Returns:
        A dict wtih data about the merge.

    """
    data = merges.merge(profile, branch, merge_into)
    return data
