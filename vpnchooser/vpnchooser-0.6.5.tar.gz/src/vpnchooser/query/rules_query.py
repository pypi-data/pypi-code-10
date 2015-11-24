# -*- encoding: utf-8 -*-

from paramiko import SSHClient, SFTPClient

from .objects import Rule


class RulesQuery(object):

    RULE_PATH = None

    def __init__(self, connection: SSHClient):
        self._ssh = connection
        self._sftp = None
        self._reset()

    def _load_rules(self):
        """
        Loads the rules from the SSH-Connection
        """
        with self._sftp_connection.open(self.RULE_PATH) as file:
            data = file.read()
        lines = (
            line.strip()
            for line in data.split('\n')
        )
        rule_strings = (
            line for line in lines
            if len(line) > 0
        )
        rules = (
            Rule.parse(rule_string)
            for rule_string in rule_strings
        )
        self._rules = [
            rule
            for rule in rules
            if rule is not None
        ]

    def _reset(self):
        """
        Resets the internal state to download
        the data from the router of the currently
        valid rules.
        """
        self._rules = None

    @property
    def rules(self):
        if self._rules is None:
            self._load_rules()
        return self._rules

    @property
    def _sftp_connection(self) -> SFTPClient:
        if self._sftp is None:
            self._sftp = self._ssh.open_sftp()
        return self._sftp

    def __del__(self):
        try:
            self._sftp.close()
        except Exception:
            pass
        try:
            self._ssh.close()
        except Exception:
            pass

    def _exec_command(self, command: str):
        """
        Executes the command and closes the handles
        afterwards.
        """
        stdin, stdout, stderr = self._ssh.exec_command(command)
        # Clearing the buffers
        stdout.read()
        stderr.read()
        stdin.close()

    def sync(self, rules: list):
        """
        Synchronizes the given rules with the server
        and ensures that there are no old rules active
        which are not in the given list.
        """
        self._reset()
        old_rules = self.rules
        to_delete_rules = [
            rule for rule in old_rules
            if rule not in rules
        ]
        new_rules = [
            rule for rule in rules
            if rule not in old_rules
        ]

        for new_rule in new_rules:
            assert isinstance(new_rule, Rule)
            self._exec_command(new_rule.add_command)
        for to_delete_rule in to_delete_rules:
            assert isinstance(to_delete_rule, Rule)
            self._exec_command(
                to_delete_rule.remove_command
            )
        self._update(rules)

    def _update(self, rules: list):
        """
        Updates the given rules and stores
        them on the router.
        """
        self._rules = rules
        to_store = '\n'.join(
            rule.config_string
            for rule in rules
        )
        sftp_connection = self._sftp_connection
        with sftp_connection.open(self.RULE_PATH, mode='w') as file_handle:
            file_handle.write(to_store)
