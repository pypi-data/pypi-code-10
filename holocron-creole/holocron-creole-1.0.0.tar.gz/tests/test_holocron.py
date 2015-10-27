# coding: utf-8

# Copyright (C) 2015  Igor Kalnitsky
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from holocron.app import Holocron
from holocron_creole.converter import Creole


class TestHolocronInstance(unittest.TestCase):
    """
    Test Creole extension is discovered by Holocron.
    """

    def setUp(self):
        self.holocron = Holocron(conf={
            'ext': {
                'enabled': ['creole'],
            },
        })

    def test_extension_is_registered(self):
        self.assertIn('creole', self.holocron._extensions)
        self.assertIsInstance(self.holocron._extensions['creole'], Creole)

    def test_converter_is_registered(self):
        self.assertIn('.creole', self.holocron._converters)
        self.assertIsInstance(self.holocron._converters['.creole'], Creole)
