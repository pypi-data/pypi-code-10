# -*- coding: utf-8 -*-

"""Basic utilities for making requests to Github's API."""

import requests
from .constants import GITHUB_API_BASE_URL


def get_url(profile, resource):
    """Get the URL for a resource."""
    repo = profile["repo"]
    url = GITHUB_API_BASE_URL + "repos/" + repo + "/git" + resource
    return url


def post_merge_request(profile, resource, payload):
    """Do a POST request to Github's API to merge."""
    repo = profile["repo"]
    url = GITHUB_API_BASE_URL + "repos/" + repo + "/merges"
    headers = get_headers(profile)
    response = requests.post(url, json=payload, headers=headers)
    return response


def get_headers(profile):
    """Get the HTTP headers needed to make Github API requests."""
    headers = {}
    headers["Authorization"] = "token " + profile["token"]
    headers["Accept"] = "application/vnd.github.v3+json"
    headers["Content-Type"] = "application/json"
    return headers


def get_request(profile, resource):
    """Do a GET request to Github's API."""
    url = get_url(profile, resource)
    headers = get_headers(profile)
    response = requests.get(url, headers=headers)
    return response.json()


def post_request(profile, resource, payload):
    """Do a POST request to Github's API."""
    url = get_url(profile, resource, is_internals)
    headers = get_headers(profile)
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def patch_request(profile, resource, payload):
    """Do a PATCH request to Github's API."""
    url = get_url(profile, resource)
    headers = get_headers(profile)
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def delete_request(profile, resource):
    """Do a DELETE request to Github's API."""
    url = get_url(profile, resource)
    headers = get_headers(profile)
    return requests.delete(url, headers=headers)
