# Copyright (c) 2013, Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# GNU Lesser General Public License version 3 (see the file LICENSE).

from StringIO import StringIO

from configglue.glue import schemaconfigglue
from configglue.parser import SchemaConfigParser
from configglue.schema import Schema, Section
from testtools import TestCase

from oops_dictconfig.configglue_options import OopsOption


class BasicSchema(Schema):

    class oops(Section):

        oops = OopsOption()


class ConfigglueOptionsTests(TestCase):

    def get_parser(self, schema_class):
        return SchemaConfigParser(schema_class())

    def get_options_from_config(self, schema_class, config):
        """`config` is a file-like object containing the config"""
        parser = self.get_parser(schema_class)
        parser.readfp(config)
        return schemaconfigglue(parser, argv=[])[1]

    def test_emtpy_gives_empty(self):
        options = self.get_options_from_config(BasicSchema,
            StringIO(""))
        self.assertEqual([], options.oops_oops['publishers'])
        self.assertEqual({}, options.oops_oops['template'])

    def test_basic_amqp_definition(self):
        options = self.get_options_from_config(BasicSchema,
            StringIO("""
[oops]
oops = oops_config

[oops_config]
publishers = amqp_publisher

[amqp_publisher]
type = amqp
host = example.com
"""))
        publishers = options.oops_oops['publishers']
        self.assertEqual(1, len(publishers))
        self.assertEqual('amqp', publishers[0]['type'])
        self.assertEqual('example.com', publishers[0]['host'])

    def test_basic_datedir_definition(self):
        options = self.get_options_from_config(BasicSchema,
            StringIO("""
[oops]
oops = oops_config

[oops_config]
publishers = datedir_publisher

[datedir_publisher]
type = datedir
error_dir = some/dir
"""))
        publishers = options.oops_oops['publishers']
        self.assertEqual(1, len(publishers))
        self.assertEqual('datedir', publishers[0]['type'])
        self.assertEqual('some/dir', publishers[0]['error_dir'])

    def test_fallback_chain(self):
        options = self.get_options_from_config(BasicSchema,
            StringIO("""
[oops]
oops = oops_config

[oops_config]
publishers = fallback_chain

[fallback_chain]
fallback_chain = amqp_publisher
                 datedir_publisher

[amqp_publisher]
type = amqp
host = example.com

[datedir_publisher]
type = datedir
error_dir = some/dir
"""))
        publishers = options.oops_oops['publishers']
        self.assertEqual(1, len(publishers))
        self.assertEqual(2, len(publishers[0]['fallback_chain']))
        fallback_chain = publishers[0]['fallback_chain']
        self.assertEqual('amqp', fallback_chain[0]['type'])
        self.assertEqual('example.com', fallback_chain[0]['host'])
        self.assertEqual('datedir', fallback_chain[1]['type'])
        self.assertEqual('some/dir', fallback_chain[1]['error_dir'])
