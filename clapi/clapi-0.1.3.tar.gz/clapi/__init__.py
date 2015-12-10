# -*- coding utf-8 -*-

import logging
from subprocess import Popen, PIPE


class MalformedHeader(Exception):
    pass


class EmptyBody(Exception):
    pass


class UnexpectedResponse(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


class Client(object):
    def __init__(self, username, password, clapi_path, debug=False):
        self.username = username
        self.password = password
        self.clapi_path = clapi_path
        self.logger = logging.getLogger('clapi_wrapper')

        if debug is True:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        # Setup console handler
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def _exec(self, argument, command, option=None):
        self.logger.debug("Executing CLAPI with %s/%s" % (option, argument))
        cmd = [self.clapi_path,
               '-u', self.username, '-p', self.password,
               '-a', argument, '-v', command]

        if option:
            cmd.extend(['-o', option])

        self.logger.debug(' '.join(cmd))

        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        cmd_output = stdout.decode('utf-8')
        cmd_error = stderr.decode('utf-8')
        if p.returncode != 0:
            raise UnexpectedResponse(cmd_output, p.returncode)

        return p.returncode

    def apply_template(self, hostname):
        self._exec(option='host', argument='applytpl', command=hostname)

    def set_snmp(self, hostname, community):
        snmp_community_str = '%s;snmp_community;%s' % (hostname, community)
        snmp_version_str = '%s;snmp_version;%s' % (hostname, '2c')
        self._exec(option='host', argument='setparam', command=snmp_community_str)
        self._exec(option='host', argument='setparam', command=snmp_version_str)

    def apply_config(self, poller):
        self._exec(option=None, argument='applycfg', command=poller)

    def set_hostgroups(self, hostname, hostgroups):
        hostgroups_str = '%s;%s' % (hostname, hostgroups)
        self._exec(option='host', argument='sethostgroup', command=hostgroups_str)

    def exclude_services(self, hostname, services):
        for service in services:
            service_str = "%(hostname)s;%(service)s;activate;0" % (
                {
                    'hostname': hostname,
                    'service': service
                }
            )
            self._exec(option='service', argument='setparam', command=service_str)

    def create_host(self, host):
        host_str = "%(hostname)s;%(fqdn)s;%(ip)s;%(templates)s;%(poller)s;%(hostgroups)s" % (
            {
                'hostname': host['hostname'],
                'fqdn': host['fqdn'],
                'ip': host['ip'],
                'templates': host['templates'],
                'poller': host['poller'],
                'hostgroups': host['hostgroups']
            }
        )

        self._exec(option='host', argument='add', command=host_str)




