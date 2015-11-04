# coding: utf-8

import copy

from apigw.api_base import ApiBase

class Iam(ApiBase):

    @classmethod
    def api_name(cls):
        return 'iam'

    @classmethod
    def require_authorization(cls):
        return True

    def get(self, path, **kwargs):
        return self.get_request(path, **kwargs)

    def post(self, path, data):
        return self.post_request(path, data=data)

    def put(self, path):
        return self.put_request(path)

    def delete(self, path):
        return self.delete_request(path)

    @classmethod
    def apply_service_name_to_args(cls, service_name, **kwargs):
        cloned_args = copy.deepcopy(kwargs)
        querys = cloned_args.get('querys', {})
        querys['serviceName'] = service_name
        cloned_args['querys'] = querys
        return cloned_args
