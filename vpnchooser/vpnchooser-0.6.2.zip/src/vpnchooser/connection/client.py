# -*- encoding: utf-8 -*-

import paramiko
import base64
import stat

from vpnchooser.applicaton import app
from vpnchooser.objects import Rule


class Client(object):
    """
    Client to connect to the router and
    synchronise with the data.
    """

    def __init__(self):
        self.rule_location = '/tmp/vpnchooser_rules/rules.txt'

    def connect(self):
        """
        Connects the client to the server and
        returns it.
        """
        key = paramiko.RSAKey(data=base64.b64decode(
            app.config['SSH_HOST_KEY']
        ))
        client = paramiko.SSHClient()
        client.get_host_keys().add(
            app.config['SSH_HOST'],
            'ssh-rsa',
            key
        )
        client.connect(
            app.config['SSH_HOST'],
            username=app.config['SSH_USER'],
            password=app.config['SSH_PASSWORD'],
        )
        return client

    def _create_directory_structure(self):
        sftp = self.client.open_sftp()
        rules = [
            rule_string
            for rule_string in
            self.rule_location.split("/")
            if len(rule_string) > 0
        ]
        checked_rules = []
        for rule in rules[:-1]:
            check_path = '/' + '/'.join(checked_rules)
            checked_rules.append(rule)
            if rule not in sftp.listdir(
                check_path
            ):
                sftp.mkdir('/' + '/'.join(checked_rules))
        sftp.close()

    @property
    def server_rules(self):
        """
        Reads the server rules from the client
        and returns it.
        """
        sftp = self.client.open_sftp()
        try:
            rule_path = self.rule_location
            try:
                stat_entry = sftp.stat(rule_path)
                if stat.S_ISDIR(stat_entry.st_mode):
                    sftp.rmdir(rule_path)
                    return []
            except IOError:
                return []
            with sftp.open(rule_path, 'r') as file_handle:
                data = file_handle.read()
            return self._parse(data)
        finally:
            sftp.close()

    @staticmethod
    def _parse(data: str) -> list:
        """
        Parses the given data string and returns
        a list of rule objects.
        """
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        lines = (
            item for item in
            (item.strip() for item in data.split('\n'))
            if len(item) and not item.startswith('#')
        )
        rules = []
        for line in lines:
            rules.append(
                Rule.parse(line)
            )
        return rules

    def sync(self, rules: list):
        """
        Synchronizes the given ruleset with the
        one on the server and adds the not yet
        existing rules to the server.
        :type rules: collections.Iterable[Rule]
        """
        self.client = self.connect()
        try:
            server_rules = set(self.server_rules)
            rules = set(rules)
            to_remove_rules = server_rules.difference(rules)
            to_add_rules = rules.difference(server_rules)
            for to_remove_rule in to_remove_rules:
                stdin, stdout, stderr = self.client.exec_command(
                    to_remove_rule.remove_command
                )
                stdout.read()
                stderr.read()
            for to_add_rule in to_add_rules:
                stdin, stdout, stderr = self.client.exec_command(
                    to_add_rule.add_command
                )
                stdout.read()
                stderr.read()

            if len(to_remove_rules) or len(to_add_rules):
                self._write_to_server(rules)
                stdin, stdout, stderr = self.client.exec_command(
                    'ip route flush cache'
                )
                stdout.read()
                stderr.read()
        finally:
            self.client.close()

    def _write_to_server(self, rules: list):
        """
        Writes the given ruleset to the
        server configuration file.
        :type rules: collections.Iterable[Rule]
        """
        self._create_directory_structure()
        config_data = '\n'.join(rule.config_string for rule in rules)
        sftp = self.client.open_sftp()
        try:
            with sftp.open(self.rule_location, 'w') as file_handle:
                file_handle.write(config_data)
                file_handle.write('\n')
        finally:
            sftp.close()
