# -*- coding: utf-8 -*-

import logging

import json
from base import Endpoint

__all__ = ['VolumeEndpoint']

class VolumeEndpoint( Endpoint ):

    _kwarg_map = {}

    @classmethod
    def volumes( cls, client ):
        r = client.get('api/volumes.json')
        return r['response']['volumes']


    @classmethod
    def volume( cls, client, volume_name ):
        r = client.get('api/volumes/%s.json' % volume_name )
        return r['response']['volume']


    @classmethod
    def servers( cls, client, volume_name ):
        r = client.get('api/volumes/%s/servers.json' % volume_name )
        return r['response']['servers']


    @classmethod
    def detach_servers( cls, client, volume_name, servers_list ):

        log = logging.getLogger(__name__)
        log.debug('detach_servers servers_list=(%s)' % servers_list)

        r = client.post(
                'api/volumes/%s/detach.json' % volume_name,
                params={ 'servers': '%s' % ','.join( servers_list ) }
                )
        return servers_list


    @classmethod
    def update_export_name( cls, client, volume_name, export_name ):
        r = client.put(
            'api/volumes/%s/export_name.json' % volume_name,
            params={ 'exportname': export_name }
            )
        return r['response']['vol_name']


    @classmethod
    def snapshot_policies( cls, client, cgroup_name ):
        r = client.get(
                'api/consistency_groups/%s/snapshot_policies.json' % cgroup_name )
        return r['response']['snapshot_policies']


    @classmethod
    def attach_snapshot_policy( cls, client, cgroup_name, policy ):
        r = client.post(
                'api/consistency_groups/%s/attach_policy.json' %
                cgroup_name, params={ 'policy': policy })
        return policy


    @classmethod
    def snapshots( cls, client, cgroup_name ):
        r = client.get( 'api/consistency_groups/%s/snapshots.json' % cgroup_name )
        return r['response']['snapshots']


    @classmethod
    def create_snapshot( cls, client, cgroup_name, snapshot_display_name ):
        r = client.post(
                'api/consistency_groups/%s/snapshots.json' % cgroup_name,
                params={ 'display_name': snapshot_display_name }
                )
        return r['response']['snapshot_name']


    @classmethod
    def clone( cls, client, cgroup_name, clone_name, snapshot_name=None ):
        """ returns the cloned cg_name or None, if successful but taking its time
        """
        log = logging.getLogger(__name__)
        log.debug('------------------------------ starting zvpsa.volume.clone ----------------------')

        data = { 'name': clone_name, 'display_name': clone_name }
        if snapshot_name is not None:
            data['snapshot'] = snapshot_name

        log.debug('BEFORE BEFORE: %s' % json.dumps(data) )

        r = client.send_request_without_response_check(
                'post',
                path='api/consistency_groups/%s/clone.json' % cgroup_name,
                params=data,
                extra_headers=client.default_headers
                )

        log.debug('AFTER AFTER: %s' % r )

        if 'response' in r.keys():
            status = int( r['response']['status'] )

            if 0 == status:
                return r['response']['cg_name']
            else:
                # it might just taking its time...
                if 'The request has been submitted' not in r['response']['message']:
                    raise ZadaraVpsaError( status, r['response']['message'] )
                else:

                    log.debug('zvpsa.volume.clone returning NONE even though it is OK!!!!!!!!!')
                    # status == 0, but it's taking its time to clone
                    return None

        raise ZadaraVpsaError( 1, 'clone() json missing "response" key' )


