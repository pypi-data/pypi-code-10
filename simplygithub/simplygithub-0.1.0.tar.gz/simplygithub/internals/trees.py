# -*- coding: utf-8 -*-

"""Utilities for getting/creating trees."""

from . import api


def prepare(data):
    """Prepare the data for output."""
    sha = data.get("sha")
    tree = data.get("tree")
    return {"sha": sha, "tree": tree}


def get_tree(profile, sha, recursive=True):
    """Get a tree."""
    resource = "/trees/" + sha
    if recursive:
        resource += "?recursive=1"
    data = api.get_request(profile, resource)
    return prepare(data)


def create_tree(profile, tree):
    """Create a new tree."""
    resource = "/trees"
    payload = {"tree": tree}
    data = api.post_request(profile, resource, payload)
    return prepare(data)
