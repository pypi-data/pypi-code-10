# -*- coding: utf-8 -*-

"""Utilities for getting/creating/listing refs."""

from . import api


def prepare(data):
    """Restructure/prepare data about refs for output."""
    ref = data.get("ref")
    obj = data.get("object")
    sha = obj.get("sha")
    return {"ref": ref, "head": {"sha": sha}}


def list_refs(profile, ref_type=None):
    """List all refs.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        ref_type
            The type of ref you want. For heads, it's ``heads``. For tags,
            it's ``tags``. That sort of thing. If you don't specify a type,
            all refs are returned.

    Returns:
        A list of dicts with data about each ref.

    """
    resource = "/refs"
    if ref_type:
        resource += "/" + ref_type
    data = api.get_request(profile, resource)
    result = [prepare(x) for x in data]
    return result


def get_ref(profile, ref):
    """Fetch a ref.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        ref
            The ref to fetch, e.g., ``heads/my-feature-branch``.

    Returns
        A dict with data about the ref.

    """
    resource = "/refs/" + ref
    data = api.get_request(profile, resource)
    return prepare(data)


def create_ref(profile, ref, sha):
    """Create a ref.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        ref
            The ref to create, e.g., ``heads/my-feature-branch``.

        sha
            The SHA of the commit to point the ref to.

    Returns
        A dict with data about the ref.

    """
    resource = "/refs"
    payload = {"ref": "refs/" + ref, "sha": sha}
    data = api.post_request(profile, resource, payload)
    return prepare(data)


def update_ref(profile, ref, sha):
    """Point a ref to a new SHA.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        ref
            The ref to update, e.g., ``heads/my-feature-branch``.

        sha
            The SHA of the commit to point the ref to.

    Returns
        A dict with data about the ref.

    """
    resource = "/refs/" + ref
    payload = {"sha": sha}
    data = api.patch_request(profile, resource, payload)
    return prepare(data)


def delete_ref(profile, ref):
    """Delete a ref.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        ref
            The ref to fetch, e.g., ``heads/my-feature-branch``.

    Returns
        The response of the DELETE request.

    """
    resource = "/refs/" + ref
    return api.delete_request(profile, resource)
