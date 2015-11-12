# -*- coding: utf-8 -*-

from base import Endpoint

__all__ = ['SnapshotPolicyEndpoint']

class SnapshotPolicyEndpoint( Endpoint ):

    @classmethod
    def snapshot_policies( cls, client ):
        r = client.get('api/snapshot_policies.json')
        return r['response']['snapshot_policies']


    @classmethod
    def snapshot_policy( cls, client, snapshot_policy_name ):
        r = client.get('api/snapshot_policies/%s.json' % unicode( snapshot_policy_name, 'utf-8' ) )
        return r['response']['snapshot_policy']






