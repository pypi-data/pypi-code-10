# PYTHON_ARGCOMPLETE_OK

from projectdb_api import projectdb_api, PROJECTDB_DEFAULT_URL, POSITIONAL_ARG_REGISTRY
from projectdb_models import *
import argparse
import os
import ConfigParser
import sys
import logging
from pprint import pprint, pformat
from booby import Model
from pyclist.pyclist import pyclist,is_api_method

CONF_FILENAME = 'proji.conf'
CONF_HOME = os.path.expanduser('~/.'+CONF_FILENAME)

class ProjiConfig(object):

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()

        try:
            user = os.environ['SUDO_USER']
            conf_user = os.path.expanduser('~'+user+"/."+CONF_FILENAME)
            candidates = [conf_user, CONF_HOME]
        except KeyError:
            candidates = [CONF_HOME]

        self.config.read(candidates)

        try:
            self.projectdb_url = self.config.get('default', 'url')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            self.projectdb_url = PROJECTDB_DEFAULT_URL

        try:
            self.projectdb_username = self.config.get('default', 'username')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            self.projectdb_username = None

        try:
            self.projectdb_token = self.config.get('default', 'token')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            self.projectdb_token = None


class Proji(object):

    def __init__(self):

        self.config = ProjiConfig()

        self.cli = pyclist('proj', 'A commandline client for CeR project management.')

        self.cli.root_parser.add_argument('--url', '-u', help='Projectdb base url', default=self.config.projectdb_url)
        self.cli.root_parser.add_argument('--username', help='Projectdb username', default=self.config.projectdb_username)
        self.cli.root_parser.add_argument('--token', help='Token to connect to figshare', default=self.config.projectdb_token)

        self.cli.root_parser.add_argument('--profile', '-p', help='Profile to use (profile must be defined in ~/.proji.conf)')


        self.cli.root_parser.add_argument('--output', '-o', help='Filter output format')
        self.cli.root_parser.add_argument('--separator', '-s', default='\n', help='Separator for output, useful to create a comma-separated list of ids. Default is new-line')

        self.cli.add_command(projectdb_api, POSITIONAL_ARG_REGISTRY)

        self.cli.parse_arguments()

        self.url = self.cli.namespace.url
        self.username = self.cli.namespace.username
        self.token = self.cli.namespace.token

        self.cli.execute()

        self.output = self.cli.namespace.output
        self.separator = self.cli.namespace.separator

        self.cli.print_result(self.output, self.separator)


def run():
    Proji()
