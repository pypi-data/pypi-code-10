# -*- coding: utf-8 -*-

"""Utilities for getting/creating commits."""

from . import api


def prepare(data):
    """Prepare the data for output."""
    message = data.get("message")
    sha = data.get("sha")
    tree = data.get("tree")
    tree_sha = tree.get("sha")
    return {"message": message, "sha": sha, "tree": {"sha": tree_sha}}


def get_commit(profile, sha):
    """Get a commit."""
    resource = "/commits/" + sha
    data = api.get_request(profile, resource)
    return prepare(data)


def create_commit(profile, message, tree, parents):
    """Create a commit."""
    resource = "/commits"
    payload = {"message": message, "tree": tree, "parents": parents}
    data = api.post_request(profile, resource, payload)
    return prepare(data)
