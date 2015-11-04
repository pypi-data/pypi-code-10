# coding: utf-8

import copy

from apigw.api_base import ApiBase

class BusinessProcess(ApiBase):

    @classmethod
    def api_name(cls):
        return 'business-process'

    @classmethod
    def require_authorization(cls):
        return True

    def get(self, path, service_name, **kwargs):
        new_args = self.__class__.apply_service_name_to_args(service_name, **kwargs)
        return self.get_request(path, **new_args)

    def post(self, path, service_name, data, **kwargs):
        new_args = self.__class__.apply_service_name_to_args(service_name, **kwargs)
        args_data = new_args.get('data', {})
        args_data.update(data)
        new_args['data'] = args_data
        return self.post_request(path, **new_args)

    @classmethod
    def apply_service_name_to_args(cls, service_name, **kwargs):
        cloned_args = copy.deepcopy(kwargs)
        querys = cloned_args.get('querys', {})
        querys['serviceName'] = service_name
        cloned_args['querys'] = querys
        return cloned_args
