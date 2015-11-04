# coding: utf-8
import json
import copy
import sys
# urlparseはPython2と3でモジュールの場所が違う
if sys.version_info[0] == 2:
    from urlparse import urlparse
if sys.version_info[0] == 3:
    from urllib.parse import urlparse

import requests

import apigw
from apigw.oauth import OAuth
from apigw.business_process import BusinessProcess
from apigw.api_log import ApiLog
from apigw.iam import Iam

class ApiGWClient(object):

    DEFAULT_CONFIG = {
        "timeout": 30000,
        "verify_ssl": False,
        "debuggable": False
    }

    def __init__(self, **kwargs):
        config = {}

        if 'config_path' in kwargs and 'environment' in kwargs:
            # 外部ファイル読み込み
            f = open(kwargs['config_path'], "r")
            cfg_all = json.load(f)
            config = cfg_all[kwargs['environment']]
            f.close()
        elif 'config' in kwargs:
            # 引数をそのまま設定として使う
            config = kwargs['config']

        self.host = config.get("host")
        if self.host is None:
            raise RuntimeError("Configuration 'host' is not found.")

        self.api_version = config.get("api_version")
        if self.api_version is None:
            raise RuntimeError("Configuration 'api_version' is not found.")

        self.verify_ssl = config.get("verify_ssl", self.DEFAULT_CONFIG["verify_ssl"])
        self.timeout = config.get("timeout", self.DEFAULT_CONFIG["timeout"])
        self.debuggable = config.get("debuggable", self.DEFAULT_CONFIG["debuggable"])

    def oauth(self, consumer_key, secret_key):
        return OAuth(self, consumer_key=consumer_key, secret_key=secret_key)

    def business_process(self, access_token):
        return BusinessProcess(self, access_token=access_token)

    def api_log(self, access_token):
        return ApiLog(self, access_token=access_token)

    def iam(self, access_token):
        return Iam(self, access_token=access_token)

    def send_request(self, method, path, **kwargs):
        cloned_args = copy.deepcopy(kwargs)
        querys = cloned_args.get('querys')
        data = cloned_args.get('data')
        headers = cloned_args.get('headers', {})

        if 'Accept' not in headers:
            headers['Accept'] = "application/json"
        if 'Host' not in headers:
            headers['Host'] = urlparse(self.host).netloc
        if 'User-Agent' not in headers:
            headers['User-Agent'] = "apigw/{0}".format(apigw.version)

        url = "{0}/{1}/{2}".format(self.host, self.api_version, path)
        timeout_sec = self.timeout / 1000
        response = requests.request(method, url,
                                    params = querys, json = data, headers = headers,
                                    timeout = timeout_sec, verify = self.verify_ssl)

        if self.debuggable:
            ApiGWClient.verbose(response)

        return response

    @classmethod
    def verbose(cls, response):
        lines = [""]
        request = response.request

        # HTTPメソッド、パス
        lines.append("{0} {1} HTTP/1.1".format(request.method, request.path_url))
        # リクエストヘッダー
        for k, v in sorted(request.headers.items()):
            lines.append("{0}: {1}".format(k, v))
        # ペイロードJSON
        lines.append(ApiGWClient.pretty_json(request.body))
        lines.append("")

        version = { 9: '0.9', 10: '1.0', 11: '1.1', 20: '2' }[response.raw._original_response.version]
        lines.append("HTTP/{0} {1} {2}".format(version, response.status_code, response.reason))
        # レスポンスヘッダー
        for k, v in sorted(response.headers.items()):
            lines.append("{0}: {1}".format(k, v))
        # レスポンスbody
        lines.append(ApiGWClient.pretty_json(response.text))
        lines.append("")

        print("\n".join(lines))

    @classmethod
    def pretty_json(cls, input):
        if input is None:
            return ''
        try:
            return json.dumps(json.loads(input), indent=2)
        except ValueError:
            pass
        return input
