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

from mock import Mock
from nose.tools import (
    assert_dict_contains_subset, assert_equal, assert_not_in, assert_raises, assert_in
)
from neutron_lbaas.services.loadbalancer.data_models import (
    LoadBalancer, Pool, HealthMonitor, Listener, SessionPersistence, Member
)

from kemptech_openstack_lbaas.driver import MapNeutronToKemp


class TestMapNeutronToKemp(object):

    def __init__(self):
        self.plugin = None
        self.context = None
        self.api_helper = None
        self._lb = None
        self.lb = None
        self._pool = None
        self.pool = None
        self._hm = None
        self.hm = None
        self.session_persistence = None
        self.listener = None

    def setup(self):
        self.plugin = Mock()
        self.context = Mock()
        self.api_helper = MapNeutronToKemp(self.plugin)
        self._lb = LoadBalancer()
        self._lb.vip_address = "10.0.0.1"
        self.lb = self._lb.to_dict()
        self.plugin.get_loadbalancer.return_value = self.lb
        self._pool = Pool()
        self.pool = self._pool.to_dict()
        self.plugin.get_pool.return_value = self.pool
        self._hm = HealthMonitor()
        self.hm = self._hm.to_dict()
        self.plugin.get_health_monitor.return_value = self.hm
        self.session_persistence = SessionPersistence()
        self.listener = Listener()

    def test_prepare_listener(self):
        self.listener.protocol_port = 80
        self.listener.protocol = "HTTP"
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 80, 'prot': 'tcp'}
        assert_equal(result, expect)

    def test_prepare_listener_pool_exists(self):
        self.listener.protocol_port = 80
        self.listener.protocol = "HTTP"
        self.listener.default_pool_id = 1
        self.pool['lb_algorithm'] = "ROUND_ROBIN"
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 80, 'schedule': 'rr', 'prot': 'tcp'}
        assert_equal(result, expect)

    def test_prepare_listener_sets_vstype(self):
        self.listener.protocol_port = 801
        self.listener.protocol = "HTTP"
        self.listener.default_pool_id = 1
        self.pool['healthmonitor_id'] = 1
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 801, 'prot': 'tcp', 'vstype': 'http'}
        assert_equal(result, expect)

    def test_prepare_listener_sets_checkuseget_is_true(self):
        self.listener.protocol_port = 80
        self.listener.protocol = "HTTP"
        self.listener.default_pool_id = 1
        self.pool['healthmonitor_id'] = 1
        self.hm['http_method'] = "GET"
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 80, 'prot': 'tcp', 'checkuseget': 1}
        assert_equal(result, expect)

    def test_prepare_listener_sets_checkuseget_is_false(self):
        self.listener.protocol_port = 80
        self.listener.protocol = "HTTP"
        self.listener.default_pool_id = 1
        self.pool['healthmonitor_id'] = 1
        self.hm['http_method'] = "POST"
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 80, 'prot': 'tcp', 'checkuseget': 0}
        assert_equal(result, expect)

    def test_prepare_listener_sets_persistence(self):
        self.listener.protocol_port = 80
        self.listener.protocol = "HTTP"
        self.listener.default_pool_id = 1
        self.pool['lb_algorithm'] = "ROUND_ROBIN"
        self.session_persistence.type = "SOURCE_IP"
        self.pool['session_persistence'] = self.session_persistence
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 80, 'schedule': 'rr', 'prot': 'tcp', 'persist': 'src'}
        assert_equal(result, expect)

    def test_prepare_listener_sets_persistence_active_cookie(self):
        self.listener.protocol_port = 80
        self.listener.protocol = "HTTP"
        self.listener.default_pool_id = 1
        self.pool['lb_algorithm'] = "ROUND_ROBIN"
        self.session_persistence.type = "APP_COOKIE"
        self.session_persistence.cookie_name = "chocolate"
        self.pool['session_persistence'] = self.session_persistence
        result = self.api_helper.prepare_listener(self.context, self.listener)
        expect = {'vs': '10.0.0.1', 'port': 80, 'schedule': 'rr', 'prot': 'tcp', 'persist': 'active-cookie', 'cookie': 'chocolate'}
        assert_equal(result, expect)

    def test_prepare_member(self):
        pass
