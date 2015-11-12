# -*- coding: utf-8 -*-

import json
from base import Endpoint

__all__ = ['ServerEndpoint']

class ServerEndpoint( Endpoint ):

    @classmethod
    def servers( cls, client ):
        r = client.get('api/servers.json')
        return r['response']['servers']

    @classmethod
    def attach_volume( cls, client, server_list, volume_name,
            access_type='NFS', readonly='NO', force='NO' ):
        if 1 > len( server_list ):
            raise ValueError( 'empty server_list not allowed' )

        data = { 'id': '%s' % ','.join( server_list ),
                'volume_name': volume_name,
                'access_type': access_type,
                'readonly': readonly,
                'force': force }

        r = client.post( 'api/servers/{0}/volumes.json'.format( server_list[0] ),
                params=data )
        return server_list


