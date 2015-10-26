# Copyright 2015 F-Secure

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You may
# obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

import time
import libvirt
from threading import Lock
import xml.etree.ElementTree as etree

from see.interfaces import Context
from see.environment import load_configuration

NOSTATE = 0
RUNNING = 1
BLOCKED = 2
PAUSED = 3
SHUTDOWN = 4
SHUTOFF = 5
CRASHED = 6
SUSPENDED = 7

STATES_MAP = {NOSTATE: (),
              RUNNING: ('pause',
                        'poweroff',
                        'forced_poweroff',
                        'restart',
                        'shutdown'),
              BLOCKED: (),
              PAUSED: ('resume',
                       'forced_poweroff'),
              SHUTDOWN: ('poweron'),
              SHUTOFF: ('poweron'),
              CRASHED: ('poweron'),
              SUSPENDED: ('resume')}


class QEMUContextFactory(object):
    def __init__(self, configuration):
        self.configuration = load_configuration(configuration)

    def __call__(self, identifier):
        from see.context.resources.qemu import QEMUResources

        resources = QEMUResources(identifier, self.configuration)
        return SeeContext(identifier, resources)


class LXCContextFactory(object):
    def __init__(self, configuration):
        self.configuration = load_configuration(configuration)

    def __call__(self, identifier):
        from see.context.resources.lxc import LXCResources

        resources = LXCResources(identifier, self.configuration)
        return SeeContext(identifier, resources)


class VBoxContextFactory(object):
    def __init__(self, configuration):
        self.configuration = load_configuration(configuration)

    def __call__(self, identifier):
        from see.context.resources.vbox import VBoxResources

        resources = VBoxResources(identifier, self.configuration)
        return SeeContext(identifier, resources)


class SeeContext(Context):
    """
    SEE Context for generic Sandbox providing through libvirt API.

    Allows to control the set of libvirt resources
    (hypervisor connection, domain, network and storage pool)
    necessary to provide a fully sandboxed environment.

    It exposes few high level method to easily instruct the sandbox.

    SeeContext is an observable, therefore it can trigger events to
    the installed plugins.

    """
    arp_table_path = '/proc/net/arp'

    def __init__(self, identifier, resources):
        super(SeeContext, self).__init__(identifier)
        self._resources = resources
        self._hypervisor_mutex = Lock()
        self._domain_mutex = Lock()
        self._storage_pool_mutex = Lock()
        self._network_mutex = Lock()
        self._mac_address = None
        self._ip4_address = None

    def cleanup(self):
        """Claims the resources back."""
        self._resources.cleanup()

    @property
    def hypervisor(self):
        """libvirt.virConnect."""
        with self._hypervisor_mutex:
            if self._resources.hypervisor.isAlive():
                return self._resources.hypervisor
            else:
                raise RuntimeError(self.identifier,
                                   "Hypervisor connection is closed")

    @property
    def domain(self):
        """libvirt.virDomain."""
        with self._domain_mutex:
            return self._resources.domain

    @property
    def storage_pool(self):
        """libvirt.virStoragePool."""
        with self._storage_pool_mutex:
            if self._resources.storage_pool.isActive():
                return self._resources.storage_pool
            else:
                raise RuntimeError(self.identifier, "Storage Pool unavailable.")

    @property
    def network(self):
        """libvirt.virNetwork."""
        with self._network_mutex:
            if self._resources.network.isActive():
                return self._resources.network
            else:
                raise RuntimeError(self.identifier, "Network is unavailable.")

    @property
    def mac_address(self):
        if self._mac_address is None:
            self._mac_address = self._get_mac_address()

        return self._mac_address

    def _get_mac_address(self):
        conf = etree.fromstring(self.domain.XMLDesc())
        mac_element = conf.find('.//devices/interface[@type="network"]/mac')

        return mac_element is not None and mac_element.get('address') or None

    @property
    def ip4_address(self):
        if self._ip4_address is None:
            self._ip4_address = self._get_ip_address()

        return self._ip4_address

    def _get_ip_address(self):
        with open(self.arp_table_path) as arp_file:
            arp_table = arp_file.read()

        return arp_table_lookup(self.mac_address, arp_table)

    def poweron(self, **kwargs):
        """
        Powers on the Context.

        Triggered events::
          * pre_poweron
          * post_poweron

        @param kwargs: keyword arguments to pass altogether with the events.

        """
        self._command('poweron', self.domain.create, **kwargs)

    def resume(self, **kwargs):
        """
        Resume the Context.

        Triggered events::
          * pre_resume
          * post_resume

        @param kwargs: keyword arguments to pass altogether with the events.

        """
        self._command('resume', self.domain.resume, **kwargs)

    def pause(self, **kwargs):
        """
        Suspend the Context.

        Triggered events::
          * pre_pause
          * post_pause

        @param kwargs: keyword arguments to pass altogether with the events.

        """
        self._command('pause', self.domain.suspend, **kwargs)

    def poweroff(self, **kwargs):
        """
        Powers off the Context. The machine is forced off immediately.

        Triggered events::
          * pre_poweroff
          * post_poweroff

        @param kwargs: keyword arguments to pass altogether with the events.

        """
        self._command('poweroff', self.domain.destroy, **kwargs)

    def shutdown(self, timeout=None, **kwargs):
        """
        Shuts down the Context. Sends an ACPI request to the OS for a clean
        shutdown.

        Triggered events::
          * pre_poweroff
          * post_poweroff

        .. note::
           The Guest OS needs to support ACPI requests sent from the host,
           the completion of the operation is not ensured by the platform.
           If the Guest OS is still running after the given timeout,
           a RuntimeError will be raised.

        @param timeout: (int) amout of seconds to wait for the machine shutdown.
        @param kwargs: keyword arguments to pass altogether with the events.

        """
        self._assert_transition('shutdown')
        self.trigger('pre_shutdown', **kwargs)
        self._execute_command(self.domain.shutdown)
        self._wait_for_shutdown(timeout)
        self.trigger('post_shutdown', **kwargs)

    def _wait_for_shutdown(self, timeout):
        if timeout is not None:
            for _ in range(timeout * 10):
                if self.domain.state()[0] == SHUTOFF:
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError("Domain shutdown timeout.")
        else:
            while self.domain.state()[0] != SHUTOFF:
                time.sleep(0.1)

    def restart(self, **kwargs):
        """Restart the Operative System within the Context.

        Triggered events::
          * pre_restart
          * post_restart

        .. note::
           The Guest OS needs to support ACPI requests sent from the host,
           the completion of the operation is not ensured by the platform.

        @param kwargs: keyword arguments to pass altogether with the events.

        """
        self._command('restart', self.domain.reboot, 0, **kwargs)

    def _command(self, event, command, *args, **kwargs):
        """
        Context state controller.

        Check whether the transition is possible or not, it executes it and
        triggers the Hooks with the pre_* and post_* events.

        @param event: (str) event generated by the command.
        @param command: (virDomain.method) state transition to impose.
        @raise: RuntimeError.

        """
        self._assert_transition(event)
        self.trigger('pre_%s' % event, **kwargs)
        self._execute_command(command, *args)
        self.trigger('post_%s' % event, **kwargs)

    def _assert_transition(self, event):
        """Asserts the state transition validity."""
        state = self.domain.state()[0]
        if event not in STATES_MAP[state]:
            raise RuntimeError("State transition %s not allowed" % event)

    def _execute_command(self, command, *args):
        """Execute the state transition command."""
        try:
            command(*args)
        except libvirt.libvirtError as error:
            raise RuntimeError("Unable to execute command. %s" % error)


def arp_table_lookup(mac_address, arp_table):
    """
    Searches the given mac address within the ARP table,
    if it finds a match it returns the IP Address.

    """
    lines = [line.split() for line in arp_table.split('\n')]

    for line in lines:
        if line and line[3] == mac_address:
            return line[0]

    return None
