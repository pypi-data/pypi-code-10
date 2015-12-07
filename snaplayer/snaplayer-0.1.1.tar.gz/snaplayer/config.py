# -*- coding: utf-8 -*-

"""
snaplayer.config
~~~~~~~~

Configuration file implementation

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.
"""

import yaml
from schema import Schema, Optional


class Config():
    """Configuration file

    Its role's very simple, to load
    a YAML file, validate it and from there
    set options to be used by this program
    """

    def __init__(self, *, config_file):
        """Constructor

        :param config_file: path to configuration file
        """

        # Default set of options
        self._options = {
            'hourly': True,
            'monthly': True,
            'tags': None,
            'cpus': None,
            'memory': None,
            'hostname': None,
            'domain': None,
            'local_disk': None,
            'datacenter': None,
            'nic_speed': None,
            'public_ip': None,
            'private_ip': None
            }

        # Validation schema for each option
        self._schema = Schema({
            Optional('hourly'): bool,
            Optional('monthly'): bool,
            Optional('tags'): lambda tags: isinstance(tags, list)
                              and all([isinstance(t, str) for t in tags]),
            Optional('cpus'): int,
            Optional('memory'): int,
            Optional('hostname'): str,
            Optional('domain'): str,
            Optional('local_disk'): str,
            Optional('datacenter'): str,
            Optional('nic_speed'): int,
            Optional('public_ip'): str,
            Optional('private_ip'): str
            })

        # Load YAML file and validate it
        with open(config_file, "r") as file:
            data = self._schema.validate(yaml.load(file))
            for key, value in data.items():
                # overwrite defaults with values taken
                # from the configuration file
                if key in self._options:
                    self._options[key] = value

    @property
    def options(self):
        """Get the whole options set"""
        return self._options
