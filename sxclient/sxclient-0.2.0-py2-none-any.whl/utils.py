'''
Auxiliary functions of the library.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

from .defaults import FILTER_NAME_TO_UUID
from .models import UserData
from .queries import ClusterSession, QueryHandler
from ._utils import generate_poll_times

__all__ = ('generate_key',
           'generate_poll_times',
           'get_cluster_uuid',
           'list_filters')

def generate_key(username, password, uuid):
    '''
    Derive user authentication key from username, password and cluster UUID.

    Note that username and password should be encoded in UTF-8.
    '''
    user_data = UserData.from_userpass_pair(username, password, uuid)
    return user_data.key

def get_cluster_uuid(cluster, verify=True):
    '''
    Obtain UUID of the cluster described by the passed Cluster object.

    Parameter 'verify' determines whether the SSL certificate used to connect
    to the cluster should be validated; the parameter value defaults to True.
    If string is be passed as a value, it is be used as a path to a custom
    trusted CA bundle for certificate verifications.
    '''
    with ClusterSession(cluster, verify=verify) as session:
        uuid = QueryHandler._get_cluster_uuid(cluster, session)
    return uuid

def list_filters():
    '''Return a list of available filters' names.'''
    return FILTER_NAME_TO_UUID.keys()
