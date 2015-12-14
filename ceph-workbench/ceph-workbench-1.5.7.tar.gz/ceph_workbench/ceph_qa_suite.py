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
from ceph_workbench.util import get_config_dir
from ceph_workbench.util import sh
import logging
import os
from scripts import openstack

log = logging.getLogger(__name__)


class CephQaSuite(object):

    def __init__(self, args, argv):
        self.args = args
        self.argv = argv

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            parents=[
                openstack.get_parser(),
            ],
            conflict_handler='resolve',
        )
        return parser

    @staticmethod
    def factory(argv):
        return CephQaSuite(
            CephQaSuite.get_parser().parse_args(argv), argv)

    def verify_keys(self):
        if (self.args.key_name or self.args.key_filename):
            return
        key_dir = get_config_dir()
        if not os.path.exists(key_dir):
            os.mkdir(key_dir)
        key_name = 'teuthology-myself'
        sh("""
        cd {key_dir}
        set -x
        if ! test -f {key_name}.pem ; then
            openstack keypair delete {key_name} || true
            openstack keypair create {key_name} > {key_name}.pem || exit 1
            chmod 600 {key_name}.pem
        fi
        if ! test -f {key_name}.pub ; then
            if ! ssh-keygen -y -f {key_name}.pem > {key_name}.pub ; then
               cat {key_name}.pub
               exit 1
            fi
        fi
        if ! openstack keypair show {key_name} > {key_name}.keypair 2>&1 ; then
            openstack keypair create --public-key {key_name}.pub {key_name} || exit 1 # noqa
        else
            fingerprint=$(ssh-keygen -l -f {key_name}.pub | cut -d' ' -f2)
            if ! grep --quiet $fingerprint {key_name}.keypair ; then
                openstack keypair delete {key_name} || exit 1
                openstack keypair create --public-key {key_name}.pub {key_name} || exit 1 # noqa
            fi
        fi
        """.format(key_dir=key_dir,
                   key_name=key_name))
        self.argv_override('--key-name', key_name)
        self.argv_override('--key-filename',
                           os.path.join(key_dir, key_name + ".pem"))

    def argv_override(self, key, value):
        symbol = key.replace('-', '_')[2:]
        exec('self.args.' + symbol + ' = "' + value + '"', globals(), locals())
        original_argv = self.argv[:]
        self.argv = []
        while len(original_argv) > 0:
            if original_argv[0] == key:
                del original_argv[0:2]
            elif original_argv[0].startswith(key):
                del original_argv[0]
            else:
                self.argv.append(original_argv.pop(0))
        self.argv.extend([key, value])

    def run(self):
        self.verify_keys()
        self.argv_override('--teuthology-branch', 'openstack')
        self.argv_override('--teuthology-git-url',
                           'http://github.com/dachary/teuthology')
        command = ("teuthology-openstack " +
                   " ".join(map(lambda x: "'" + x + "'", self.argv[1:])))
        return sh(command)
