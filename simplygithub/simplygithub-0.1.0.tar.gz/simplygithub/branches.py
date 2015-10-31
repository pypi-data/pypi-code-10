# -*- coding: utf-8 -*-

"""Utilities for getting/creating/listing branches."""

from .internals import (merges, refs)


def get_branch_sha(profile, name):
    """Get the SHA a branch's HEAD points to."""
    ref = "heads/" + name
    data = refs.get_ref(profile, ref)
    head = data.get("head")
    sha = head.get("sha")
    return sha


def list_branches(profile):
    """List all branches."""
    data = refs.list_refs(profile, ref_type="heads")
    return data


def get_branch(profile, name):
    """Get a branch."""
    ref = "heads/" + name
    data = refs.get_ref(profile, ref)
    return data


def create_branch(profile, name, branch_off):
    """Create a branch."""
    branch_off_sha = get_branch_sha(profile, branch_off)
    ref = "heads/" + name
    data = refs.create_ref(profile, ref, branch_off_sha)
    return data


def update_branch(profile, name, sha):
    """Move a branch's HEAD to a new SHA."""
    ref = "heads/" + name
    data = refs.update_ref(profile, ref, sha)
    return data


def delete_branch(profile, name):
    """Delete a branch."""
    ref = "heads/" + name
    data = refs.delete_ref(profile, ref)
    return data


def merge(profile, branch, base_branch):
    """Merge a branch into a base branch."""
    data = merges.merge(profile, branch, base_branch)
    return data
