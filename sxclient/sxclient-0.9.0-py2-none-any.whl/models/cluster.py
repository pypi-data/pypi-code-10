'''
Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.
'''
from requests.compat import urlunparse

from sxclient.tools import toutf8

__all__ = ['Cluster']


class Cluster(object):
    '''
    Store cluster connection parameters and provide connection data for cluster
    and its specific nodes.

    Initialization parameters:
      - name -- name of the cluster; used as a domain name to connect to the
        cluster in absence of ip_address
      - ip_address -- IP address of a node belonging to the cluster; if set,
        used to connect to the cluster instead of cluster name
      - is_secure -- flag determining whether the connection will be secured by
        SSL
      - port -- custom remote port to connect to; if unset, default ports will
        be used (443 for https, 80 for http)
    '''

    def __init__(
        self, name, ip_address=None, is_secure=True, port=None
    ):
        self.name = toutf8(name)
        self.ip_address = None
        if ip_address is not None:
            self.ip_address = toutf8(ip_address)
        self.is_secure = is_secure
        self.port = int(port) if port is not None else None

    @property
    def url(self):
        return self.get_host_url(self.host)

    def get_host_url(self, host):
        '''Get URL for a node host specified in the argument.'''
        data = (self.scheme, self.get_host_netloc(host), '', '', '', '')
        url = urlunparse(data)
        return url

    @property
    def host(self):
        return self.ip_address if self.ip_address else self.name

    @property
    def scheme(self):
        if self.is_secure:
            scheme = 'https'
        else:
            scheme = 'http'
        return scheme

    def get_host_netloc(self, host):
        '''
        Get network location (host + port) for a node host specified in the
        argument.
        '''
        if self.port is not None:
            netloc = ':'.join((host, str(self.port)))
        else:
            netloc = host
        return netloc
