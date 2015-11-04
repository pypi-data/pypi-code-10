# coding: utf-8

import copy

class ApiBase(object):

    @classmethod
    def api_name(cls):
        raise NotImplementedError()

    @classmethod
    def require_authorization(cls):
        return False

    def __init__(self, client, consumer_key=None, secret_key=None, access_token=None):
        self.client = client
        self.consumer_key = consumer_key
        self.secret_key = secret_key
        self.access_token = access_token

    def get_request(self, path, **kwargs):
        return self.__request('GET', path, **kwargs)

    def post_request(self, path, **kwargs):
        return self.__request('POST', path, **kwargs)

    def put_request(self, path, **kwargs):
        return self.__request('PUT', path, **kwargs)

    def delete_request(self, path, **kwargs):
        return self.__request('DELETE', path, **kwargs)

    def options_request(self, path, **kwargs):
        return self.__request('OPTIONS', path, **kwargs)

    def __request(self, method, path, **kwargs):
        cls = self.__class__
        if path is None:
            url = cls.api_name()
        else:
            url = "{0}/{1}".format(cls.api_name(), path)

        cloned_args = copy.deepcopy(kwargs)
        if cls.require_authorization():
            headers = cloned_args.get('headers', {})
            headers['Authorization'] = "Bearer {0}".format(self.access_token)
            cloned_args['headers'] = headers

        return self.client.send_request(method, url, **cloned_args)
