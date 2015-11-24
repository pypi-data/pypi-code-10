# -*- encoding: utf-8 -*-

import re


parse_rule = re.compile('^(?P<ip>[0-9\.a-fA-F/]+) (?P<table>[0-9]+)$')


class Rule(object):
    """
    A rule which is bound to a table and an ip
    address range.
    """

    def __init__(self, ip=None, table=None):
        self.ip = ip
        self.table = table

    @property
    def add_command(self) -> str:
        if self.ip is None or self.table is None:
            return
        return "ip rule add from {ip} table {table}".format(
            **self.__dict__
        )

    @property
    def remove_command(self) -> str:
        if self.ip is None or self.table is None:
            return
        return "ip rule del from {ip} table {table}".format(
            **self.__dict__
        )

    @property
    def config_string(self) -> str:
        if self.ip is None or self.table is None:
            return
        return "{ip} {table}".format(
            **self.__dict__
        )

    @classmethod
    def parse(cls, line: str):
        match = parse_rule.match(line)
        if match is None:
            return None

        rule = cls()
        rule.ip = match.group('ip')
        rule.table = match.group('table')
        return rule

    def __eq__(self, other):
        if not isinstance(other, Rule):
            return False
        return other.ip == self.ip and other.table == self.table

    def __hash__(self):
        return self.ip.__hash__() + self.table.__hash__() ** 32
