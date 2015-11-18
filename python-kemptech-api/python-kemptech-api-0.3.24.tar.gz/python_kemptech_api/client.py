import os
import subprocess
import logging

import requests
import requests.packages
from requests import exceptions

from .api_xml import (
    get_error_msg, is_successful,
    get_data_field, parse_to_dict)
from .exceptions import (
    KempTechApiException,
    CommandNotAvailableException,
    ConnectionTimeoutException)

from .exceptions import LoadMasterParameterError

requests.packages.urllib3.disable_warnings()
log = logging.getLogger(__name__)


class HttpClient(object):
    """Client that performs HTTP requests."""

    ip_address = None
    endpoint = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def _do_request(self, http_method, rest_command,
                    parameters=None,
                    file=None):
        """Perform a HTTP request.

        :param http_method: GET or POST.
        :param rest_command: The command to run.
        :param parameters: dict containing parameters.
        :param file: Location of file to send.
        :return: The Status code of request and the response text body.
        """
        response = None
        cmd_url = "{endpoint}{cmd}?".format(endpoint=self.endpoint,
                                            cmd=rest_command)
        log.debug("Request is: %s", cmd_url)

        try:
            if file is not None:
                with open(file, 'rb') as payload:
                    response = requests.request(http_method, cmd_url,
                                                params=parameters,
                                                verify=False,
                                                data=payload)
            else:
                response = requests.request(http_method, cmd_url,
                                            params=parameters,
                                            timeout=5,
                                            verify=False)
            if 400 < response.status_code < 500:
                raise KempTechApiException(code=response.status_code)
            else:
                response.raise_for_status()
        except exceptions.ConnectTimeout:
            log.error("The connection timed out to %s.", self.ip_address)
            raise ConnectionTimeoutException(self.ip_address)
        except exceptions.ConnectionError:
            log.error("A connection error occurred to %s.", self.ip_address)
            raise
        except exceptions.URLRequired:
            log.error("%s is an invalid URL", cmd_url)
            raise
        except exceptions.TooManyRedirects:
            log.error("Too many redirects with request to %s.", cmd_url)
            raise
        except exceptions.Timeout:
            log.error("A connection %s has timed out.", self.ip_address)
            raise
        except exceptions.HTTPError:
            log.error("A HTTP error occurred with request to %s.", cmd_url)
            raise KempTechApiException(msg=response.text,
                                       code=response.status_code)
        except exceptions.RequestException:
            log.error("An error occurred with request to %s.", cmd_url)
            raise
        return response.text

    def _get(self, rest_command, parameters=None):
        return self._do_request('GET', rest_command, parameters)

    def _post(self, rest_command, file=None, parameters=None):
        return self._do_request('POST', rest_command, parameters=parameters,
                                file=file)

# ---- LoadMaster ---


def send_response(response):
    if is_successful(response):
        return parse_to_dict(response)
    else:
        raise KempTechApiException(get_error_msg(response))


class LoadMaster(HttpClient):
    """LoadMaster API object."""

    def __init__(self, ip, username, password, port=443):
        self.ip_address = ip
        self.username = username
        self.password = password
        self.port = port

    def __repr__(self):
        return '{}:{}'.format(self.ip_address, self.port)

    @property
    def endpoint(self):
        return "https://{user}:{pw}@{ip}:{port}/access".format(
            user=self.username,
            pw=self.password,
            ip=self.ip_address,
            port=self.port
        )

    def set_parameter(self, parameter, value):
        parameters = {
            'param': parameter,
            'value': value,
        }
        response = self._get('/set', parameters)
        if not is_successful(response):
            raise LoadMasterParameterError(self, parameters)

    def get_parameter(self, parameter):
        parameters = {
            'param': parameter,
        }
        response = self._get('/get', parameters)
        value = get_data_field(response, parameter)
        if isinstance(value, dict):
            # This hack converts possible HTML to an awful one string
            # disaster instead of returning parsed html as an OrderedDict.
            value = "".join("{!s}={!r}".format(key, val) for (key, val) in
                            sorted(value.items()))
        return value

    def enable_api(self):
        """Enable LoadMaster API"""
        # Can't use the HttpClient methods for this as the
        # endpoint is different when attempting to enable the API.
        url = ("https://{user}:{pw}@{ip}:{port}"
               "/progs/doconfig/enableapi/set/yes").format(user=self.username,
                                                           pw=self.password,
                                                           ip=self.ip_address,
                                                           port=self.port)
        try:
            requests.get(url, verify=False, timeout=1)
            return True
        except exceptions.RequestException:
            return False

    def stats(self):
        response = self._get('/stats')
        return send_response(response)

    def update_firmware(self, file):
        response = self._post('/installpatch', file)
        return is_successful(response)

    def shutdown(self):
        response = self._get('/shutdown')
        return is_successful(response)

    def reboot(self):
        response = self._get('/reboot')
        return is_successful(response)

    def get_sdn_controller(self):
        response = self._get('/getsdncontroller')
        return send_response(response)

    def get_license_info(self):
        try:
            response = self._get('360/licenseinfo')
            return send_response(response)

        except KempTechApiException:
            raise CommandNotAvailableException(
                self, '/access360/licenseinfo')

    def list_addons(self):
        response = self._get('/listaddon')
        return send_response(response)

    def upload_template(self, file):
        response = self._post('/uploadtemplate', file)
        return send_response(response)

    def list_templates(self):
        response = self._get('/listtemplates')
        return send_response(response)

    def delete_template(self, template_name):
        params = {'name': template_name}
        response = self._get('/deltemplate', parameters=params)
        return send_response(response)

    def apply_template(self, virtual_ip, port, protocol, template_name):
        params = {
            'vs': virtual_ip,
            'port': port,
            'prot': protocol,
            'name': template_name,
        }
        response = self._get('/addvs', parameters=params)
        return send_response(response)

    def get_sdn_info(self):
        response = self._get('/sdninfo')
        return send_response(response)

    def restore_backup(self, backup_type, file):
        # 1 LoadMaster Base Configuration
        # 2 Virtual Service Configuration
        # 3 GEO Configuration
        if backup_type not in [1, 2, 3]:
            backup_type = 2
        params = {"type": backup_type}
        response = self._post('/restore', file=file,
                              parameters=params)
        return send_response(response)

    def backup(self):
        # Dirty API, dirty hack.

        if not os.path.exists('backups'):
            os.makedirs('backups')
        file_name = "backups/{}.backup".format(self.ip_address)

        with open(file_name, 'wb') as file:
            curl = ['curl', '-k', '{}/backup'.format(self.endpoint)]
            subprocess.call(curl, stdout=file)
        return file_name

    def alsi_license(self, kemp_id, password):
        params = {
            "kemp_id": kemp_id,
            "password": password,
        }
        response = self._get('/alsilicense', parameters=params)
        return send_response(response)

    def set_initial_password(self, password):
        params = {"passwd": password}
        response = self._get('/set_initial_password', parameters=params)
        return send_response(response)

    def kill_asl_instance(self):
        response = self._get('/killaslinstance')
        return send_response(response)
