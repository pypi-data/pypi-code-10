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
        ❏Eupompos❏ ./main.py
        ________________________________________________________________________

        CLI for the Eupompos project.

        Command line invocation : see documentation : 'command line invocation'
        about exit codes, see documentation : 'exit codes'
        ________________________________________________________________________

        o init_settings_from_cfgfile()
        o main()
"""

# something's wrong with the way pylint understands the import statement :
# pylint: disable=import-error

# something's wrong with the way pylint understands the import statement :
# pylint: disable=no-name-in-module
import re

#///////////////////////////////////////////////////////////////////////////////
def init_settings_from_cfgfile(settings, configfile):
    """
        init_settings_from_cfgfile()
        ________________________________________________________________________

        Initialization of some global variables from the data stored in the
        configuration file.
        ________________________________________________________________________

        no PARAMETER

        RETURN VALUE : ( (bool) success, (str)error message)
    """
    split_no_empty_elements = \
       lambda sourcestr: [element for element in sourcestr.split(";") if len(element.strip()) > 0]

    res = (True, "")

    try:
        settings.REGEX__PYTHON_FILENAMES = \
          re.compile(configfile.CONFIGDATA["python parser"]["filenames to be analysed"])
        settings.REGEX__PYTHON_FUNCTIONDECLARATION = \
          re.compile(configfile.CONFIGDATA["python parser"]["function declaration"])
        settings.REGEX__PYTHON_CHARS_IN_USEFULLCOM = \
          re.compile(configfile.CONFIGDATA["python parser"]["expected chars in a usefull comment"])
        settings.REGEX__PYTHON_CLASSDECLARATION = \
          re.compile(configfile.CONFIGDATA["python parser"]["class declaration"])
        settings.REGEX__PYTHON_DOCSTRING = \
          re.compile(configfile.CONFIGDATA["python parser"]["docstring"])
        settings.REGEX__PYTHON_DOCSTRING_UL = \
          re.compile(configfile.CONFIGDATA["python parser"]["docstring.unique line"])

        settings.REGEX__CPP_CODE_FILENAMES = \
          re.compile(configfile.CONFIGDATA["cpp parser"]["code filenames to be analysed"])
        settings.REGEX__CPP_FUNCTIONDECLARATION = \
          re.compile(configfile.CONFIGDATA["cpp parser"]["function declaration"])
        settings.REGEX__CPP_CHARS_IN_USEFULLCOM = \
          re.compile(configfile.CONFIGDATA["cpp parser"]["expected chars in a usefull comment"])

        settings.FULLNAME_BLACKLIST = \
          split_no_empty_elements(configfile.CONFIGDATA["parser"]["fullname blacklist"])

        settings.PARSERREPORT__FUNCPOS_MAXLENGTH = \
          int(configfile.CONFIGDATA["parser report"]["function position.max length"])

    except KeyError as exception:
        res = (False, "missing keyword : {0}".format(exception))

    return res

#///////////////////////////////////////////////////////////////////////////////
def main():
    """
        main()
        ________________________________________________________________________

        Main entry point.
        ________________________________________________________________________

        no PARAMETER, no RETURNED VALUE

        see the exit codes at documentation : 'exit codes' .
    """
    import sys
    from eupompos.messages import MSG

    import eupompos.cmdlineparser
    eupompos.cmdlineparser.ARGS = eupompos.cmdlineparser.CommandLineParser().get_args()

    # first welcome message :
    MSG.welcome0()

    import eupompos.settings as settings
    settings.SOURCEPATH = eupompos.cmdlineparser.ARGS.sourcepath
    settings.VERBOSITY = eupompos.cmdlineparser.ARGS.verbosity
    settings.CONFIGFILENAME = eupompos.cmdlineparser.ARGS.configfile

    # second welcome message :
    MSG.welcome1()

    import eupompos.configfile as configfile
    if not configfile.read_configfile(settings.CONFIGFILENAME):
        # see documentation : exit codes
        sys.exit(-1)

    settings_ok, settings_err = init_settings_from_cfgfile(settings, configfile)
    if not settings_ok:
        MSG.error("Can't read the configuration file : " \
                  "an error occured while reading it; error message :")
        MSG.error(settings_err)
        # see documentation : exit codes
        sys.exit(-1)

    from eupompos.parser import Parser
    # let's read the source :
    data = Parser(settings.SOURCEPATH)
    print(data.report)

    # exit code ok, see documentation : 'exit codes' .
    sys.exit(0)

if __name__ == '__main__':
    main()
