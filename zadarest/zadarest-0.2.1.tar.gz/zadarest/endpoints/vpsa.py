# -*- coding: utf-8 -*-

from base import Endpoint

__all__ = ['VpsaEndpoint']

class VpsaEndpoint(Endpoint):

    @classmethod
    def vpsas(cls, client):
        resp_data = client.send_request_without_response_check('get', 'api/vpsas.json')
        if 'vpsas' in resp_data.keys():
            return resp_data['vpsas']
        else:
            return []

    @classmethod
    def vpsa(cls, client, vpsa_id):
        vpsa_data = client.send_request_without_response_check(
                'get',
                'api/vpsas/%d.json' % vpsa_id )
        if 'vpsa' in vpsa_data.keys():
            return vpsa_data['vpsa']
        else:
            return None

    @classmethod
    def hibernate(cls, client, vpsa_id):
        h = { 'Content-Length': 0 }
        resp = client.send_request_without_response_check(
                'post',
                'api/vpsas/%d/hibernate.json' % vpsa_id,
                extra_headers=h )
        if 'response' in resp.keys():
            return resp['response']
        else:
            return 'VPSA being put into hibernating state... wait for vpsa(%d)...' % vpsa_id

    @classmethod
    def restore(cls, client, vpsa_id):
        h = { 'Content-Length': 0 }
        resp = client.send_request_without_response_check(
                'post',
                '/api/vpsas/%d/restore.json' % vpsa_id,
                extra_headers=h )
        if 'response' in resp.keys():
            return resp['response']
        else:
            return 'VPSA restoring... wait for vpsa(%d)...' % vpsa_id

