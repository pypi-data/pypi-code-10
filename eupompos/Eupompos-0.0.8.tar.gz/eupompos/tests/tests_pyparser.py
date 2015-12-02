#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#    Eupompos Copyright (C) 2012 Xavier Faure
#    Contact: suizozukan arrobas orange dot fr
#
#    This file is part of Eupompos.
#    Eupompos is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Eupompos is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Eupompos.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
        ❏Eupompos❏ ./tests/tests_pyparser.py
        ________________________________________________________________________

        Tests of the pyparser.py script
        ________________________________________________________________________

        o TestsPyParser class
"""
# something's wrong with the way pylint understands the import statement :
# pylint: disable=import-error
import unittest
import os.path

from   eupompos.parser import Parser
import eupompos.configfile as configfile
import eupompos.settings as settings
import eupompos.main

configfile.read_configfile(os.path.join("eupompos", "tests", "eupompos1.ini"))
eupompos.main.init_settings_from_cfgfile(settings, configfile)

################################################################################
class TestsPyParser(unittest.TestCase):
    """
        TestsPyParser class
        ________________________________________________________________________

	Testing the pypparser.py script
        ________________________________________________________________________

        class attributes : -

        instance attributes : -

        class methods :

            o test__functions()
    """

    #//////////////////////////////////////////////////////////////////////////
    def test__functions(self):
        """
		TestsStrTools.test__functions()
                ________________________________________________________________

		Test of the parsing of the functions.
                ________________________________________________________________

                no PARAMETER, no RETURN VALUE
        """
        # let's read the source :
        data = Parser(os.path.join("eupompos", "tests", "pyfiles001"))
        self.assertEqual(len(data.report.functions), 4)
