'''
Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.
'''
import requests

from sxclient.query.auth import SXAuth
from sxclient.query.hostname_adapter import SXHostnameAdapter


class ClusterSession(requests.Session):
    '''
    Custom session object used by a QueryHandler object.

    Initialization parameters:
      - cluster -- Cluster data structure; cluster.name is used for SSL
        verification
      - user_data -- UserData object used for authentication
      - verify -- parameter indicating whether the SSL certificate should be
        validated; defaults to True. If string is be passed as a value, it is
        be used as a path to a custom trusted CA bundle for certificate
        verifications.
    '''

    def __init__(self, cluster, user_data=None, verify=True):
        super(ClusterSession, self).__init__()
        self.mount('https://', SXHostnameAdapter(assert_hostname=cluster.name))
        if user_data is not None:
            self.auth = SXAuth(user_data)
        self.verify = verify
