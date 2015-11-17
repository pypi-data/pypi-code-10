# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2015 <contact@redhat.com>
#
# Author: Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see `<http://www.gnu.org/licenses/>`.
#
import argparse
import logging
import subprocess

log = logging.getLogger(__name__)


def sh(command):
    log.debug(command)
    output = ''
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                         shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
        raise e
    finally:
        log.debug(command + " output " + str(output))
    return output.decode('utf-8')


class CommaSplit(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))


def get_parser():
        parser = argparse.ArgumentParser(
            description="Ceph",
            add_help=False,
        )

        parser.add_argument('--releases',
                            action=CommaSplit,
                            default=[],
                            help=('Comma separated list of releases '
                                  '(e.g. dumpling,firefly)'))
        return parser


def releases():
    return ('argonaut', 'bobtail', 'cuttlefish',
            'dumpling', 'emperor', 'firefly',
            'giant', 'hammer', 'infernalis',
            'jewel', 'kraken')
