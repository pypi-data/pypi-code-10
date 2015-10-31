# -*- coding: utf-8 -*-

"""Utilities for getting/creating blobs."""

from . import api


def prepare(data):
    """Prepare the data for output."""
    sha = data.get("sha")
    content = data.get("content")
    encoding = data.get("encoding")
    return {"sha": sha, "content": content, "encoding": encoding}


def get_blob(profile, sha):
    """Get a blob."""
    resource = "/blobs/" + sha
    data = api.get_request(profile, resource)
    return prepare(data)


def create_blob(profile, content):
    """Create a blob."""
    resource = "/blobs"
    payload = {"content": content}
    data = api.post_request(profile, resource, payload)
    return data  # prepare(data)
