# -*- coding: utf8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from . import __version__, __agent__
import requests
import json

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus


class RedlinkClient(object):
    """
    Redlink generic client, internally handling all details of the communication with the Redlink API.
    """

    endpoint = "https://api.redlink.io"
    datahub = "http://data.redlink.io"
    param_key = "key"
    param_in = "in"
    param_out = "out"

    def __init__(self, key):
        """
        @param key: api key
        @return:
        """
        self.key = key
        self.version = self._get_api_version()
        self.user_agent = __agent__

        status = self.get_status()
        if not (status and status["accessible"]):
            raise ValueError("invalid key")
        else:
            self.status = status

    def _build_url(self, endpoint="", params={}):
        if len(endpoint) > 0 and not endpoint.startswith("/"):
            endpoint = "/%" % endpoint

        url = "%s/%s%s?%s=%s" % (self.endpoint, self.version, endpoint, self.param_key, self.key)
        for k, v in params.items():
            #TODO: create a wrapper for send back both uri and params to use later in responses' methods
            url += "&%s=%s" % (k, quote_plus(v))
        return url

    def _get_api_version(self):
        versions = __version__.split(".")
        return "%s.%s" % (versions[0], versions[1])

    def get_status(self):
        """
        Get api status of the current key

        @rtype: dict
        @return: status
        """
        response = self._get(self._build_url(), accept="application/json")
        if response.status_code != 200:
            return None
        else:
            return json.loads(response.text)

    def _get(self, resource, accept=None):
        headers = {"User-Agent": self.user_agent}
        if accept:
            headers["Accept"] = accept
        return requests.get(resource, headers=headers)

    def _post(self, resource, payload=None, contentType=None, accept=None):
        headers = {"User-Agent": self.user_agent}
        if contentType:
            headers["Content-Type"] = contentType
        if accept:
            headers["Accept"] = accept
        return requests.post(resource, data=payload, headers=headers)

    def _put(self, resource, payload=None, contentType=None, accept=None):
        headers = {"User-Agent": self.user_agent}
        if contentType:
            headers["Content-Type"] = contentType
        if accept:
            headers["Accept"] = accept
        return requests.put(resource, data=payload, headers=headers)

    def _delete(self, resource):
        return requests.delete(resource)
