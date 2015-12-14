#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from mock import Mock, patch, PropertyMock

from nose.tools import (
    assert_dict_contains_subset, assert_equal, assert_not_in, assert_raises
)
import requests
from requests.exceptions import RequestException

from kemptech_openstack_lbaas.client import (
    BaseKempModel, KempClientRequestError
)


class TestBaseKempModel(object):

    def __init__(self):
        self.loadbalancer = None
        self.parameters = None
        self.base_kemp = None

    def setup(self):
        self.loadbalancer = "https://bal:2fourall@10.154.190.110:443/access/"
        self.parameters = {
            "param1": 0,
            "param2": "hello, world",
            "param3": 34,
            "param4": -22,
            "param5": "",
            "param6": None,
            "param7": True,
            "param8": False,
        }
        self.base_kemp = BaseKempModel(self.loadbalancer, self.parameters)

    def test_to_dict(self):
        response_params = self.base_kemp.to_dict()
        # A copy of the setup() parameters minus the entries with value None
        parameters = {
            "param1": 0,
            "param2": "hello, world",
            "param3": 34,
            "param4": -22,
            "param5": "",
            "param7": True,
            "param8": False,
        }
        assert_dict_contains_subset(parameters, response_params)

    def test_to_dict_doesnt_contain_id(self):
        response_params = self.base_kemp.to_dict()
        assert_not_in("id", response_params)

    def test_to_dict_doesnt_contain_api_name(self):
        self.base_kemp.api_name = "vs"
        response_params = self.base_kemp.to_dict()
        assert_not_in("api_name", response_params)

    def test_get_request_raises(self):
        with patch.object(requests, "get") as get:
            get.side_effect = RequestException()
            assert_raises(KempClientRequestError, self.base_kemp._get_request,
                          "get", {"param": "version"})
