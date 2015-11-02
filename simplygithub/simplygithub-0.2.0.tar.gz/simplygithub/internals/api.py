# -*- coding: utf-8 -*-

"""Basic utilities for making requests to Github's API.

This package contains functions that can make GET, POST, PATCH, and DELETE
requests to Github's API. It also has a special method for POSTing a merge
request to Github's API.

These functions are very generic in that they simply pass the payload they
are given to the specified Github API resource, then they decode and return
the response that comes back.

Other packages do the work of preparing the correct payload, and stipulating
which Github API resource to send that payload to. But they do not send that
payload themselves. They ask this package to do it.

"""

import requests
from .constants import GITHUB_API_BASE_URL


def get_url(profile, resource):
    """Get the URL for a resource.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        resource
            The part of a Github API URL that comes after ``.../:repo/git``.
            For instance, for ``.../:repo/git/commits``, it's ``/commits``.

    Returns:
        The full URL for the specified resource under the specified profile.

    """
    repo = profile["repo"]
    url = GITHUB_API_BASE_URL + "repos/" + repo + "/git" + resource
    return url


def post_merge_request(profile, payload):
    """Do a POST request to Github's API to merge.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        payload
            A dict of information to pass to Github's API as the payload for
            a merge request, something like this::

                { "base": <base>, "head": <head>, "commit_message": <mesg>}

    Returns:
        The response returned by the ``requests`` library when it does the
        POST request.

    """
    repo = profile["repo"]
    url = GITHUB_API_BASE_URL + "repos/" + repo + "/merges"
    headers = get_headers(profile)
    response = requests.post(url, json=payload, headers=headers)
    return response


def get_headers(profile):
    """Get the HTTP headers needed to make Github API requests.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

    Returns:
        A dictionary of headers.

    """
    headers = {}
    headers["Authorization"] = "token " + profile["token"]
    headers["Accept"] = "application/vnd.github.v3+json"
    headers["Content-Type"] = "application/json"
    return headers


def get_request(profile, resource):
    """Do a GET request to Github's API.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        resource
            The part of a Github API URL that comes after ``.../:repo/git``.
            For instance, for ``.../:repo/git/commits``, it's ``/commits``.

    Returns:
        The body of the response, converted from JSON into a Python dict.

    """
    url = get_url(profile, resource)
    headers = get_headers(profile)
    response = requests.get(url, headers=headers)
    return response.json()


def post_request(profile, resource, payload):
    """Do a POST request to Github's API.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        resource
            The part of a Github API URL that comes after ``.../:repo/git``.
            For instance, for ``.../:repo/git/commits``, it's ``/commits``.

        payload
            A dict of values to send as the payload of the POST request.
            The data will be JSON-encoded.

    Returns:
        The body of the response, converted from JSON into a Python dict.

    """
    url = get_url(profile, resource)
    headers = get_headers(profile)
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def patch_request(profile, resource, payload):
    """Do a PATCH request to Github's API.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        resource
            The part of a Github API URL that comes after ``.../:repo/git``.
            For instance, for ``.../:repo/git/commits``, it's ``/commits``.

        payload
            A dict of values to send as the payload of the POST request.
            The data will be JSON-encoded.

    Returns:
        The body of the response, converted from JSON into a Python dict.

    """
    url = get_url(profile, resource)
    headers = get_headers(profile)
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def delete_request(profile, resource):
    """Do a DELETE request to Github's API.

    Args:

        profile
            A profile generated from ``simplygithub.authentication.profile``.
            Such profiles tell this module (i) the ``repo`` to connect to,
            and (ii) the ``token`` to connect with.

        resource
            The part of a Github API URL that comes after ``.../:repo/git``.
            For instance, for ``.../:repo/git/commits``, it's ``/commits``.

    Returns:
        The response returned by the ``requests`` library when it does the
        POST request.

    """
    url = get_url(profile, resource)
    headers = get_headers(profile)
    return requests.delete(url, headers=headers)
