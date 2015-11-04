# coding: utf-8

from apigw.api_base import ApiBase

class OAuth(ApiBase):

    @classmethod
    def api_name(cls):
        return 'oauth'

    def request_access_token(self):
        data = { "grantType": "client_credentials",
                 "clientId": self.consumer_key,
                 "clientSecret": self.secret_key }
        return self.post_request('accesstokens', data=data)
