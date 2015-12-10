import os
from urllib import quote
from urlparse import urljoin


def get_host_name():
    host_name = os.environ.get('HTTP_HOST', os.environ.get('SERVER_NAME', ''))
    if ':' in host_name:
        host_name = host_name[:host_name.find(':')]
    return host_name


def get_host_url():
    protocol = os.environ.get('wsgi.url_scheme')
    if not protocol:
        if os.environ.get('HTTPS') == 'on':
            protocol = 'https'
        else:
            protocol = 'http'
    hostname = os.environ.get(
        'HTTP_HOST', os.environ.get('SERVER_NAME', 'localhost'))
    port = os.environ.get('SERVER_PORT', '')

    url = '://'.join([protocol, hostname])
    if port and not ':' in hostname:
        if protocol == 'https' and port != '443':
            url += ':' + port
        if protocol == 'http' and port != '80':
            url += ':' + port
    return url


def build_absolute_uri(location):
    """ Returns the absolute URI form of location. """
    return urljoin(get_host_url(), quote(location))


def get_dict(post, key):
    """ Extract from POST PHP-like arrays as dictionary.

        Example usage::

            <input type="text" name="option[key1]" value="Val 1">
            <input type="text" name="option[key2]" value="Val 2">

            options = get_dict(request.POST, 'option')
            options['key1'] is 'Val 1'
            options['key2'] is 'Val 2'
    """
    result = {}
    if post:
        import re
        patt = re.compile('^([a-zA-Z_]\w+)\[([a-zA-Z_\-][\w\-]*)\]$')
        for post_name, value in post.items():
            value = post[post_name]
            match = patt.match(post_name)
            if not match or not value:
                continue
            name = match.group(1)
            if name == key:
                k = match.group(2)
                result.update({k: value})
    return result
