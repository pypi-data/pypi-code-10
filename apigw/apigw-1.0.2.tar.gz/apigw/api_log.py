# coding: utf-8

from apigw.api_base import ApiBase

class ApiLog(ApiBase):

    @classmethod
    def api_name(cls):
        return 'apilog'

    @classmethod
    def require_authorization(cls):
        return True

    def get(self, target_date):
        querys = { 'targetDate': target_date }
        return self.get_request(None, querys=querys)
