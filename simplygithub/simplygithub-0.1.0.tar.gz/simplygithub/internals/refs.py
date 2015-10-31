# -*- coding: utf-8 -*-

"""Utilities for getting/creating/listing refs."""

from . import api


def prepare(data):
    """Prepare the data for output."""
    ref = data.get("ref")
    obj = data.get("object")
    sha = obj.get("sha")
    return {"ref": ref, "head": {"sha": sha}}


def list_refs(profile, ref_type=None):
    """List all refs."""
    resource = "/refs"
    if ref_type:
        resource += "/" + ref_type
    data = api.get_request(profile, resource)
    result = []
    for item in data:
        record = prepare(item)
        result.append(record)
    return result


def get_ref(profile, ref):
    """Get a branch."""
    resource = "/refs/" + ref
    data = api.get_request(profile, resource)
    return prepare(data)


def create_ref(profile, ref, sha):
    """Create a ref."""
    resource = "/refs"
    payload = {"ref": "refs/" + ref, "sha": sha}
    data = api.post_request(profile, resource, payload)
    return prepare(data)


def update_ref(profile, ref, sha):
    """Point a ref to a new SHA."""
    resource = "/refs/" + ref
    payload = {"sha": sha}
    data = api.patch_request(profile, resource, payload)
    return prepare(data)


def delete_ref(profile, ref):
    """Delete a ref."""
    resource = "/refs/" + ref
    return api.delete_request(profile, resource)
