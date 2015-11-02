# -*- coding: utf-8 -*-

"""Utilities for getting/creating blobs."""

from . import api


def prepare(data):
    """Restructure/prepare data about blobs for output."""
    sha = data.get("sha")
    content = data.get("content")
    encoding = data.get("encoding")
    return {"sha": sha, "content": content, "encoding": encoding}


def get_blob(profile, sha):
    """Fetch a blob.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        sha
            The SHA of the blob to fetch.

    Returns:
        A dict with data about the blob.

    """
    resource = "/blobs/" + sha
    data = api.get_request(profile, resource)
    return prepare(data)


def create_blob(profile, content):
    """Create a blob.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        content
            The (UTF-8 encoded) content to create in the blob.

    Returns:
        A dict with data about the newly created blob.

    """
    resource = "/blobs"
    payload = {"content": content}
    data = api.post_request(profile, resource, payload)
    return data
