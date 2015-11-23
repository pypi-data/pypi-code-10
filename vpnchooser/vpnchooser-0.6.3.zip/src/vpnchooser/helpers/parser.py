# -*- encoding: utf-8 -*-

from urllib.parse import urlparse
from werkzeug.exceptions import NotFound

from vpnchooser.applicaton import app


def id_from_url(url, param_name: str) -> int:
    """
    Parses an object and tries to extract a url.
    Tries to parse if a resource_url has been given
    it as a url.
    :raise ValueError: If no id could be extracted.
    """
    if url is None:
        raise ValueError('url is none')
    elif isinstance(url, int):
        # Seems to already be the url.
        return url
    if not url:
        raise ValueError('Seems to be empty')

    try:
        return int(url)
    except ValueError:
        pass

    parsed = urlparse(url)
    try:
        resource_url = app.url_map.bind(parsed.netloc).match(
            parsed.path
        )
    except NotFound:
        raise ValueError('No URL found')

    if param_name in resource_url[1]:
        return resource_url[1][param_name]
    else:
        raise ValueError(
            'Parameter {name} could not be extracted'.format(
                name=param_name
            )
        )
