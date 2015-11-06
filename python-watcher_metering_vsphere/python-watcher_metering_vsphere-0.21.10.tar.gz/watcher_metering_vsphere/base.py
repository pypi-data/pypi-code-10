# -*- encoding: utf-8 -*-
# Copyright (c) 2015 b<>com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

from oslo_config import cfg
from oslo_log import log
from watcher_metering.agent.measurement import Measurement
from watcher_metering.agent.puller import MetricPuller
from watcher_metering_vsphere.wrappers.vsphere import VSphereWrapper

LOG = log.getLogger(__name__)


class BaseVSphereMetricPuller(MetricPuller):

    metric_name = NotImplemented  # Should be contained in the above list
    metric_type = NotImplemented
    metric_unit = NotImplemented
    pulling_interval = NotImplemented

    def __init__(self, title, probe_id, interval,
                 host, username, password):
        super(BaseVSphereMetricPuller, self).__init__(
            title=title,
            probe_id=probe_id,
            interval=interval,
        )
        self._host = host
        self.wrapper = VSphereWrapper(
            host=self._host,
            username=username,
            password=password,
        )

    @classmethod
    def get_normalized_name(cls):
        return cls.metric_name.replace(".", "_")

    @classmethod
    def get_name(cls):
        return "vsphere_{0}".format(cls.get_normalized_name())

    @classmethod
    def get_default_probe_id(cls):
        return "vsphere.{0}".format(cls.get_normalized_name())

    @classmethod
    def get_metric_type(cls):
        # either 'gauge', 'cumulative' or 'delta'
        return cls.metric_type

    @classmethod
    def get_default_interval(cls):
        return cls.pulling_interval  # In seconds

    @property
    def unit(self):
        return self.metric_unit

    @classmethod
    def get_config_opts(cls):
        return cls.get_base_opts() + [
            cfg.StrOpt(
                'datacenter',
                help='vSphere datacenter FQDN or IP address'),
            cfg.StrOpt(
                'username',
                help='vSphere username (make sure the account '
                     'has the proper permissions)'),
            cfg.StrOpt(
                'password',
                secret=True,
                help='vSphere password'),
        ]

    @classmethod
    def validate(cls, measurement):
        """Should make some assertions to make sure the value is correct
        :raises: AssertionError
        """
        assert measurement
        assert measurement.unit == cls.metric_unit
        assert measurement.type == cls.metric_type

    def do_pull(self):
        LOG.info("[%s] Pulling measurements...", self.key)
        measurements = []
        for instance in self.wrapper.get_all_instances():
            LOG.info(
                "[%s] Running metric collection on instance %s ",
                self.key, instance
            )
            try:
                raw_measurement = self.wrapper.pull_metric(
                    metric_name=self.metric_name,
                    instance=instance,
                )
                LOG.debug("[%s] Formatting measurement...", self.key)
                measurement = self.format_measurement(raw_measurement)
                measurements.append(measurement)
                # Sends the measurements explicitly now
                # self.send_measurements(site_measurements)
            except KeyError as exc:
                LOG.debug("[%s] Metric not available", self.metric_name)
            except Exception as exc:
                LOG.exception(exc)
            else:
                LOG.info("[%s] Probed all VMs from `%s`", self.key, self._host)

        # We return an empty list because we want to send the data as we go
        # to avoid having to send a too large set at the end (avoid a spike).
        return measurements

    def format_measurement(self, raw_measurement):
        try:
            resource_metadata = {
                "host": raw_measurement["host_id"],
                "host_name": raw_measurement["host_name"],
                "title": self.title,
                "resource_name": raw_measurement["instance_name"],
            }
            measurement = Measurement(
                name=self.probe_id,
                unit=self.unit,
                type_=raw_measurement["type"],
                value=raw_measurement["value"],
                resource_id=raw_measurement["instance_id"],
                timestamp=raw_measurement["timestamp"],
                host=raw_measurement["host_id"],
                resource_metadata=resource_metadata,
            )
            self.validate(measurement)
            # Adds the measurements if it has been validated
            return measurement
        except Exception as exc:
            LOG.exception(exc)
