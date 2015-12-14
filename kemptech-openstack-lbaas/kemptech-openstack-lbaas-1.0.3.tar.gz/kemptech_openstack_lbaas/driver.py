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

import logging

from oslo_config import cfg
from neutron_lbaas.services.loadbalancer import constants as lb_constants
from neutron_lbaas.drivers import driver_base

from kemptech_openstack_lbaas import client
from kemptech_openstack_lbaas.client import KempClientRequestError
from kemptech_openstack_lbaas import config
from kemptech_openstack_lbaas import constants as kemp_consts

LOG = logging.getLogger(__name__)
cfg.CONF.register_opts(config.KEMP_OPTS, 'kemptechnologies')
CONF = cfg.CONF.kemptechnologies


class LoadBalancerManager(driver_base.BaseLoadBalancerManager):

    def __init__(self, driver):
        super(LoadBalancerManager, self).__init__(driver)
        self.client = self.driver.client
        self.api_helper = self.driver.api_helper

    def create(self, context, lb):
        LOG.debug("KEMP driver create lb: %s", repr(lb))
        self.driver.openstack_driver.load_balancer.successful_completion(
            context, lb)

    def update(self, context, old_lb, lb):
        LOG.debug("KEMP driver update lb: %s", repr(lb))

    def delete(self, context, lb):
        LOG.debug("KEMP driver delete lb: %s", repr(lb))
        #prep_lb = self.api_helper.prepare_loadbalancer(lb)
        #self.client.delete_virtual_services(prep_lb)
        self.driver.openstack_driver.load_balancer.successful_completion(
            context, lb, delete=True)

    def refresh(self, context, lb):
        LOG.debug("KEMP driver refresh lb: %s", repr(lb))
        # TODO(smcgough) Compare to back end and fix inconsistencies.
        self.client.refresh_loadbalancer(lb)

    def stats(self, context, lb):
        LOG.debug("KEMP driver stats of lb: %s", repr(lb))
        # TODO(smcgough) Return nothing for now.
        stats = {
            lb_constants.STATS_IN_BYTES: 0,
            lb_constants.STATS_OUT_BYTES: 0,
            lb_constants.STATS_ACTIVE_CONNECTIONS: 0,
            lb_constants.STATS_TOTAL_CONNECTIONS: 0,
        }
        return stats


class ListenerManager(driver_base.BaseListenerManager):

    def __init__(self, driver):
        super(ListenerManager, self).__init__(driver)
        self.client = self.driver.client
        self.api_helper = self.driver.api_helper

    def create(self, context, listener):
        LOG.debug("KEMP driver create listener: %s", repr(listener))
        prep_listener = self.api_helper.prepare_listener(context, listener)
        try:
            self.client.create_virtual_service(prep_listener)
            self.driver.openstack_driver.listener.successful_completion(
                context, listener
            )
        except KempClientRequestError:
            self.driver.openstack_driver.listener.failed_completion(context,
                                                                    listener)

    def update(self, context, old_listener, listener):
        LOG.debug("KEMP driver update listener: %s", repr(listener))
        old_prep_listener = self.api_helper.prepare_listener(context,
                                                             old_listener)
        prep_listener = self.api_helper.prepare_listener(context, listener)
        self.client.update_virtual_service(old_prep_listener, prep_listener)

    def delete(self, context, listener):
        LOG.debug("KEMP driver delete listener: %s", repr(listener))
        prep_listener = self.api_helper.prepare_listener(context, listener)
        self.client.delete_virtual_service(prep_listener)
        self.driver.openstack_driver.listener.successful_completion(
            context, listener, delete=True)


class PoolManager(driver_base.BasePoolManager):

    def __init__(self, driver):
        super(PoolManager, self).__init__(driver)
        self.client = self.driver.client
        self.api_helper = self.driver.api_helper

    def create(self, context, pool):
        LOG.debug("KEMP driver create pool: %s", repr(pool))
        self.driver.openstack_driver.pool.successful_completion(context, pool)

    def update(self, context, old_pool, pool):
        LOG.debug("KEMP driver update pool: %s", repr(pool))
        if old_pool['lb_method'] != pool['lb_method']:
            prep_pool = self.api_helper.prepare_pool(pool)
            self.client.update_virtual_service(prep_pool)
            self.driver.openstack_driver.pool.successful_completion(context,
                                                                    pool)

    def delete(self, context, pool):
        LOG.debug("KEMP driver delete pool: %s", repr(pool))
        prep_pool = self.api_helper.prepare_pool(pool)
        self.client.delete_virtual_service(prep_pool)
        self.driver.openstack_driver.pool.successful_completion(context, pool,
                                                                delete=True)


class MemberManager(driver_base.BaseMemberManager):

    def __init__(self, driver):
        super(MemberManager, self).__init__(driver)
        self.client = self.driver.client
        self.api_helper = self.driver.api_helper

    def create(self, context, member):
        LOG.debug("KEMP driver create member: %s", repr(member))
        prep_member = self.api_helper.prepare_member(member)
        try:
            self.client.create_real_server(prep_member)
            self.driver.openstack_driver.member.successful_completion(context,
                                                                      member)
        except KempClientRequestError:
            self.driver.openstack_driver.member.failed_completion(context,
                                                                  member)

    def update(self, context, old_member, member):
        LOG.debug("KEMP driver update member: %s", repr(member))
        old_prep_member = self.api_helper.prepare_member(old_member)
        prep_member = self.api_helper.prepare_member(member)
        try:
            self.client.update_real_server(old_prep_member, prep_member)
            self.driver.openstack_driver.member.successful_completion(context,
                                                                      member)
        except KempClientRequestError:
            self.driver.openstack_driver.member.failed_completion(context,
                                                                  member)

    def delete(self, context, member):
        LOG.debug("KEMP driver delete member: %s", repr(member))
        prep_member = self.api_helper.prepare_member(member)
        try:
            self.client.delete_real_server(prep_member)
            self.driver.openstack_driver.member.successful_completion(
                context, member, delete=True
            )
        except KempClientRequestError:
            self.driver.openstack_driver.member.failed_completion(context,
                                                                  member)


class HealthMonitorManager(driver_base.BaseHealthMonitorManager):

    def __init__(self, driver):
        super(HealthMonitorManager, self).__init__(driver)
        self.client = self.driver.client
        self.api_helper = self.driver.api_helper

    def create(self, context, health_monitor):
        LOG.debug("create_pool_health_monitor. health_monitor['type']: %s",
                  health_monitor['type'])
        check_params = self._get_health_check_params(health_monitor)
        if "http" in health_monitor['type']:
            params = self.api_helper.prepare_health_monitor(health_monitor)
            check_params.update(params)
        try:
            self.client.update_health_check(check_params)
            self.api_helper.health_monitor(health_monitor)
            self.driver.openstack_driver.health_monitor.successful_completion(
                context, health_monitor)
        except KempClientRequestError:
            self.driver.openstack_driver.health_monitor.failed_completion(
                context, health_monitor)

    def update(self, context, old_health_monitor, health_monitor):
        LOG.debug("KEMP driver update health_monitor: %s",
                  repr(health_monitor))
        check_params = self._get_health_check_params(health_monitor)
        if "http" in health_monitor['type']:
            params = self.api_helper.prepare_health_monitor(health_monitor)
            check_params.update(params)
        try:
            self.client.update_health_check(check_params)
            self.driver.openstack_driver.health_monitor.successful_completion(
                context, health_monitor)
        except KempClientRequestError:
            self.driver.openstack_driver.health_monitor.failed_completion(
                context, health_monitor)

    def delete(self, context, health_monitor):
        LOG.debug("KEMP driver delete health_monitor: %s",
                  repr(health_monitor))
        check_params = self._get_health_check_params(health_monitor)
        if "http" in health_monitor['type']:
            params = self.api_helper.prepare_health_monitor(health_monitor)
            check_params.update(params)
        try:
            self.client.update_health_check(check_params)
            self.driver.openstack_driver.health_monitor.successful_completion(
                context, health_monitor, delete=True)
        except KempClientRequestError:
            self.driver.openstack_driver.health_monitor.failed_completion(
                context, health_monitor, delete=True)

    @staticmethod
    def _get_health_check_params(health_monitor):
        """Return health check parameters from a health monitor."""
        check_params = {
            'retryinterval': health_monitor['delay'],
            'timeout': health_monitor['timeout'],
            'retrycount': health_monitor['max_retries'],
        }
        return check_params


class MapNeutronToKemp(object):

    MAP_NEUTRON_MODEL_TO_VS = {
        'vip_address': 'vs',
        'protocol_port': 'port',
        'protocol': 'prot',
        'lb_algorithm': 'schedule',
        'type': 'checktype',
        'http_method': 'checkuseget',
        'url_path': 'checkurl',
    }

    MAP_NEUTRON_MODEL_TO_RS = {
        'address': 'rs',
        'protocol_port': 'rsport',
        'weight': 'weight',
    }

    def __init__(self, plugin):
        self.plugin = plugin

    def prepare_listener(self, context, listener):
        models = [listener.to_dict()]
        loadbalancer = self.plugin.get_loadbalancer(context,
                                                    listener.loadbalancer_id)
        pool = None
        models.append(loadbalancer)
        if listener.default_pool_id is not None:
            pool = self.plugin.get_pool(context, listener.default_pool_id)
            LOG.debug(repr(listener))
            LOG.debug(repr(pool))
            models.append(pool)
        if pool is not None:
            if pool['healthmonitor_id'] is not None:
                health_mon = self.plugin.get_health_monitor(
                    context,
                    pool['healthmonitor_id']
                )
                models.append(health_mon)
        vs_params = {}

        for model in models:
            for key, value in model.items():
                if value is None:
                    continue
                try:
                    vs_key = self.MAP_NEUTRON_MODEL_TO_VS[key]
                except KeyError:
                    continue
                if key == "lb_algorithm":
                    vs_params[vs_key] = kemp_consts.LB_METHODS[value]
                elif key == "http_method":
                    if model['http_method'] == "GET":
                        vs_params[vs_key] = 1
                    else:
                        vs_params[vs_key] = 0
                else:
                    vs_params[vs_key] = value

        try:
            # Need to explicitly set vstype if port and
            # protocol do not meet default requirements
            if ("HTTP" in vs_params['prot'] and
                    vs_params['port'] != 80 and
                    vs_params['port'] != 443):
                vs_params['vstype'] = 'http'
        except KeyError:
            pass
        finally:
            # Change protocol to tcp as openstack never maps to anything else.
            vs_params['prot'] = 'tcp'

        try:
            if pool is not None and pool['session_persistence'] is not None:
                for session_persist in lb_constants.SUPPORTED_SP_TYPES:
                    if session_persist == pool['session_persistence'].type:
                        persistence = kemp_consts.PERSIST_OPTS[session_persist]
                        vs_params['persist'] = persistence
                        if persistence == kemp_consts.PERS_ACT_COOKIE:
                            cookie = pool['session_persistence'].cookie_name
                            vs_params['cookie'] = cookie
        except AttributeError:
            pass  # No pool exists
        return vs_params

    def prepare_member(self, member):
        rs_params = {}
        for key, value in member.__dict__.items():
            if value is None:
                continue
            try:
                rs_params[self.MAP_NEUTRON_MODEL_TO_RS[key]] = value
            except KeyError:
                continue
        for model in [member.pool.listener.to_dict(),
                      member.pool.listener.loadbalancer.to_dict()]:
            for key, value in model.items():
                if key in kemp_consts.VS_ID:
                    if key == "prot":
                        rs_params[self.MAP_NEUTRON_MODEL_TO_VS[key]] = "tcp"
                    if value is None:
                        continue
                    try:
                        rs_params[self.MAP_NEUTRON_MODEL_TO_VS[key]] = value
                    except KeyError:
                        continue
        return rs_params

    def prepare_health_monitor(self, context, health_monitor):
        prep_lister = self.prepare_listener(context,
                                            health_monitor.pool.listener)
        return prep_lister


class KempLoadMasterDriver(driver_base.LoadBalancerBaseDriver):
    """KEMPtechnologies LBaaS driver."""

    def __init__(self, openstack_driver, conf):
        self.openstack_driver = openstack_driver
        self.plugin = self.openstack_driver.plugin
        self.api_helper = MapNeutronToKemp(self.plugin)
        try:
            self.address = conf.lm_address
            self.username = conf.lm_username
            self.password = conf.lm_password
            self.check_interval = conf.check_interval
            self.connect_timeout = conf.connect_timeout
            self.retry_count = conf.retry_count
            self.client = client.KempClient(self.address, self.username,
                                            self.password)
        except (cfg.NoSuchOptError, client.KempClientRequestError) as error:
            LOG.error(error)
        self.load_balancer = LoadBalancerManager(self)
        self.listener = ListenerManager(self)
        self.pool = PoolManager(self)
        self.member = MemberManager(self)
        self.health_monitor = HealthMonitorManager(self)
        super(KempLoadMasterDriver, self).__init__(self.plugin)

    @property
    def default_checker_settings(self):
        """Return default health check parameters."""
        return {
            'retryinterval': self.check_interval,
            'timeout': self.connect_timeout,
            'retrycount': self.retry_count,
        }
