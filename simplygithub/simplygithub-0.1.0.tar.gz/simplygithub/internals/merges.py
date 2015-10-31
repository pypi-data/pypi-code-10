# -*- coding: utf-8 -*-

"""Utilities for performing merges."""

from . import api


def prepare(data):
    """Prepare the data for output."""
    sha = data.get("sha")
    commit = data.get("commit")
    message = commit.get("message")
    tree = commit.get("tree")
    tree_sha = tree.get("sha")
    return {"message": message, "sha": sha, "tree": {"sha": tree_sha}}


def merge(profile, head, base, commit_message=None):
    """Merge the head of a branch into the base branch."""
    resource = "/merges"
    if not commit_message:
        commit_message = "Merged " + head + " into " + base + "."
    payload = {
        "base": base,
        "head": head,
        "commit_message": commit_message,
        }
    response = api.post_merge_request(profile, resource, payload)
    data = None
    if response.status_code == 201:
        json_data = response.json()
        data = prepare(json_data)
    return data
        
