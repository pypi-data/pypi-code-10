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

import abc
import logging

import requests
from requests.exceptions import RequestException

from kemptech_openstack_lbaas import constants as kemp_consts

LOG = logging.getLogger(__name__)


class KempClient(object):

    def __init__(self, address, username, password):
        if (address is None or
                username is None or
                password is None):
            raise KempClientRequestError(msg="Missing URL credentials.")
        else:
            self.loadbalancer = ("https://{user}:{passwd}@{ip}/access/"
                                 .format(user=username, passwd=password,
                                         ip=address))
            LOG.debug("set loadmaster URL settings %s", self.loadbalancer)
            self.virtual_services = []
            self.real_servers = []

    def create_virtual_service(self, params):
        virtual_service = VirtualService(self.loadbalancer, params)
        try:
            virtual_service.create()
            self.virtual_services.append(virtual_service)
        except KempClientRequestError:
            raise

    def update_virtual_service(self, old_params, params, batch_update=False):
        old_virtual_service = VirtualService(self.loadbalancer, old_params)
        virtual_service = VirtualService(self.loadbalancer, params)
        try:
            if batch_update:
                pass
            else:
                for service in self.virtual_services:
                    if service.id == old_virtual_service.id:
                        service.update(virtual_service.to_dict())
                        self.virtual_services.remove(old_virtual_service)
                        self.virtual_services.append(virtual_service)
        except KempClientRequestError:
            raise

    def delete_virtual_service(self, params):
        virtual_service = VirtualService(self.loadbalancer, params)
        try:
            for service in self.virtual_services:
                if service.id == virtual_service.id:
                    service.delete()
        except KempClientRequestError:
            raise

    def delete_virtual_services(self):
        try:
            for virtual_service in self.virtual_services:
                virtual_service.delete()
        except KempClientRequestError:
            raise

    def create_real_server(self, params):
        """Attach a real server to a virtual service."""
        real_server = RealServer(self.loadbalancer, params)
        try:
            real_server.create()
            self.real_servers.append(real_server)
        except KempClientRequestError:
            raise

    def update_real_server(self, old_params, params):
        """Update a real server's parameters on a virtual service."""
        old_real_server = RealServer(self.loadbalancer, old_params)
        real_server = RealServer(self.loadbalancer, params)
        try:
            for server in self.real_servers:
                if server.id == old_real_server.id:
                    server.update(real_server.to_dict())
                    self.real_servers.remove(old_real_server)
                    self.real_servers.append(real_server)
        except KempClientRequestError:
            raise

    def delete_real_server(self, params):
        """Delete a real server from a virtual service."""
        real_server = RealServer(self.loadbalancer, params)
        try:
            for server in self.real_servers:
                if server.id == real_server.id:
                    server.delete()
        except KempClientRequestError:
            raise

    def update_health_check(self, check_params):
        """Update health check parameters for virtual services."""
        # pop the checker params, call update vs
        # create a health and a vs object
        checkers = {}
        for checker in kemp_consts.CHECKER_OPTS:
            checkers.update(check_params.popitem(checker))
        health_monitor = HealthMonitor(self.loadbalancer, checkers)
        try:
            health_monitor.update(health_monitor)
            virtual_service = VirtualService(self.loadbalancer, check_params)
            for service in self.virtual_services:
                if service.id == virtual_service.id:
                    service.update(virtual_service.to_dict())
        except KempClientRequestError:
            raise


class BaseKempModel(object):
    """A class to build objects based on KEMP RESTful API.

    Subclasses built from this class need to name their parameters
    the same as their RESTful API counterpart in order for this
    class to work.
    """

    def __init__(self, loadbalancer, parameters):
        self.api_name = ""  # Subclasses must define this.
        self.loadbalancer = loadbalancer
        for api_key, api_value in parameters.items():
            self.__dict__[api_key] = api_value

    def create(self):
        try:
            self._get_request('add' + self.api_name, self.to_dict())
        except KempClientRequestError:
            raise

    def update(self, obj):
        try:
            if self.exists:
                # Remove the ID parameters and update the attributes.
                for model_id in self.id:
                    if model_id in obj.__dict__:
                        obj.__dict__.pop(model_id)
                self.__dict__.update(obj.__dict__)
                self._get_request('mod' + self.api_name, self.to_dict())
        except KempClientRequestError:
            raise

    def delete(self):
        try:
            if self.exists:
                self._get_request('del' + self.api_name, self.id)
        except KempClientRequestError:
            raise

    @property
    def exists(self):
        """ runs a GET request against an API object to see if it exists

        :return: returns True when response status code is in 200 range.
        """
        return self._get_request('show' + self.api_name, self.id) < 300

    @abc.abstractproperty
    def id(self):
        """Must return a dict with unique ID parameters for KEMP API."""
        pass

    @id.setter
    @abc.abstractmethod
    def id(self, value):
        pass

    def to_dict(self):
        """Return a dictionary containing attributes of class.

        Ignore attributes that are set to None or are not a string or int;
        also ignore id as it is not an API thing.
        """
        attributes = {}
        for attr, value in self.__dict__.items():
            if value is None:
                continue
            if attr != 'id' and attr != 'api_name' and attr != 'loadmaster':
                attributes[attr] = value
        return attributes

    def _get_request(self, cmd, params):
        """Perform a HTTP GET.

        :param cmd: The command to run.
        :param params: Dict containing parameters.
        :return: Tuple of the status code of request and the response body.
        """
        cmd_url = self.loadbalancer + cmd
        LOG.debug("command being requested: %s", cmd)
        LOG.debug("GET request parameters are: %s", repr(params))

        try:
            response = requests.get(cmd_url, params=params, verify=False)
            if response.status_code > 299:
                raise RequestException
        except RequestException as exception:
            LOG.exception(exception)
            raise KempClientRequestError()
        return response.status_code, response.text


class VirtualService(BaseKempModel):

    def __init__(self, loadbalancer, parameters):
        self.vs = None
        self.rs = None
        self.port = None
        self.prot = None
        self.vsport = None
        self.rsport = None
        self.id = parameters
        super(VirtualService, self).__init__(loadbalancer, parameters)
        self.api_name = 'vs'

    @property
    def id(self):
        return {
            'vs': self.vs,
            'port': self.port,
            'prot': self.prot,
        }

    @id.setter
    def id(self, value):
        self.vs = value['vs']
        try:
            self.port = value['port']
        except KeyError:
            self.port = "80"
        try:
            self.prot = value['prot']
        except KeyError:
            self.prot = "tcp"
        try:
            self.rs = value['rs']
        except KeyError:
            self.rs = None
        try:
            self.rsport = value['rsport']
        except KeyError:
            self.rsport = None

    def update(self, virtual_service):
        if self.vsport is not None:
            if super(VirtualService, self).update(virtual_service) < 300:
                self.port = self.vsport
                self.vsport = None
        else:
            super(VirtualService, self).update(virtual_service)


class RealServer(BaseKempModel):

    def __init__(self, loadbalancer, parameters):
        self.vs = None
        self.rs = None
        self.port = None
        self.prot = None
        self.rsport = None
        self.id = parameters
        super(RealServer, self).__init__(loadbalancer, parameters)
        self.api_name = 'rs'

    @property
    def id(self):
        return {
            'vs': self.vs,
            'port': self.port,
            'prot': self.prot,
            'rs': self.rs,
            'rsport': self.rsport,
        }

    @id.setter
    def id(self, value):
        self.rs = value['rs']
        try:
            self.rsport = value['rsport']
        except KeyError:
            self.rsport = 80


class HealthMonitor(BaseKempModel):

    def __init__(self, loadbalancer, parameters):
        self.vs = None
        self.rs = None
        self.port = None
        self.prot = None
        self.rsport = None
        self.id = parameters
        super(HealthMonitor, self).__init__(loadbalancer, parameters)
        self.api_name = 'health'

    @property
    def id(self):
        """HealthMonitor's do not have a unique ID as they are global"""
        return None

    @id.setter
    def id(self, value):
        self.vs = value.get('vs', '')
        self.rs = value.get('rs', '')
        self.port = value.get('port', '')
        self.prot = value.get('prot', '')
        self.rsport = value.get('rsport', '')


class KempClientRequestError(Exception):
    """Raised if HTTP request has failed."""

    def __init__(self, code=None, msg=None):
        if msg is None:
            if code == 400:
                msg = "Mandatory parameter missing from request."
            elif code == 401:
                msg = "Username or password is missing or is incorrect."
            elif code == 403:
                msg = "Incorrect permissions."
            elif code == 404:
                msg = "Not found."
            elif code == 405:
                msg = "Unknown command."
            elif code == 422:
                msg = "Invalid parameter"
            else:
                msg = "An unknown error has occurred."
        self.message = "KEMP client error: {}".format(msg)
        super(KempClientRequestError, self).__init__()
