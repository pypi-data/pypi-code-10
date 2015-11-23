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
        ❏Eupompos❏ eupompos/pyparser.py
        ________________________________________________________________________

        parser for the Python language.
        ________________________________________________________________________

        o PyParser class
"""
# something's wrong with the way pylint understands the import statement :
# pylint: disable=import-error

from eupompos.pyparserstate import PyParserState
from eupompos.liaf import LIAF
from eupompos.messages import MSG
from eupompos.parsertools import FunctionName
import eupompos.settings as settings

import re

################################################################################
class PyParser(object):
    """
        PyParser class
        ________________________________________________________________________

        Use this class to parse a C++ file.
        ________________________________________________________________________

        class attributes : -

        instance attribute(s) : -

            o current_liaf  : a LIAF object
            o report        : a ParserReport object (the object to be filled)
            o state         : a PyParserState

        class methods :

            o __init__()
            o parse()
            o parse__class_declaration()
            o parse__function_declaration()
            o parse__empty_line()
            o parse__sharp_line()
            o reset()
            o usefull_comment_line()            (static)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, _report):
        """
                PyParser.__init__()
                ________________________________________________________________

                Set some variables to their default value.
                ________________________________________________________________

                PARAMETERS :

                    o (str)_report     : the ParserReport object to be filled.

                RETURN VALUE : None
        """
        self.report = _report

        self.current_liaf = None        # a LIAF object
        self.state = None               # a PyParserState object

    #///////////////////////////////////////////////////////////////////////////
    def parse(self, _filename, _srccontent):
        """
                PyParser.parse()
                ________________________________________________________________

                Parse a file's content and fill self.report.
                ________________________________________________________________

                PARAMETER :
                    o (str)_filename   : source file's name
                    o (str)_srccontent : the content of the file to be parsed

                RETURN VALUE : None
        """
        MSG.debug("PyParser.parse : parsing {0}...".format(_filename))

        self.reset()

        self.current_liaf.filename = _filename

        for _linenumber, _line in enumerate(_srccontent):

            linenumber = _linenumber+1

            self.current_liaf.linenumber = linenumber
            self.current_liaf.line = _line

            MSG.debug("PyParser.parse() "
                      ": filename={0}; line#{1}={2}".format(self.current_liaf.filename,
                                                            self.current_liaf.linenumber,
                                                            self.current_liaf.line))

            if re.search(settings.REGEX__PYTHON_CLASSDECLARATION,
                         self.current_liaf.line) is not None:
                self.parse__class_declaration()

            if self.current_liaf.line.startswith("#"):
                self.parse__sharp_line()

            # about function declaration :
            #
            # o   REGEX__FUNCTIONDECLARATION
            # o   no ";" at the end of the line
            # o   no space at the beginning of _line
            #
            elif re.search(settings.REGEX__PYTHON_FUNCTIONDECLARATION,
                           self.current_liaf.line) is not None:
                self.parse__function_declaration()

            else:
                # whatever was the line, it wasn't a comment. So we may
                # consider this line not being a part of the preceding block
                # of comments.
                self.state.current_block_of_comments.clear()

    #///////////////////////////////////////////////////////////////////////////
    #
    # parse__* functions
    #
    #   These functions return nothing and take no parameter.
    #
    #///////////////////////////////////////////////////////////////////////////

    #...........................................................................
    def parse__class_declaration(self):
        """
                PyParser.parse__class_declaration()
                ________________________________________________________________

                A member of the parse__* functions (see general indications
                above).

                Function called when the parser reads a class declaration.
        """
        MSG.debug("PyParser.parse__class_declaration()")
        self.state.current_class = re.search(settings.REGEX__PYTHON_CLASSDECLARATION,
                                             self.current_liaf.line).group(1)

    #...........................................................................
    def parse__function_declaration(self):
        """
                PyParser.parse__function_declaration()
                ________________________________________________________________

                A member of the parse__* functions (see general indications
                above).

                Function called when the parser reads a function declaration.
        """
        MSG.debug("PyParser.parse__function_declaration()")

        func_name = re.search(settings.REGEX__PYTHON_FUNCTIONDECLARATION,
                              self.current_liaf.line).group(1)

        # if the line doesn't start with a space, it means that it's not a class method :
        if not(self.current_liaf.line.startswith(" ") or self.current_liaf.line.startswith("\b")):
            self.state.current_class = None

        self.state.current_function = FunctionName(self.state.current_class,
                                                   func_name)

        self.report.functions[self.state.current_function] = \
          (self.current_liaf,
           [line for line in self.state.current_block_of_comments if \
                                                 self.usefull_comment_line(line)])

        self.state.current_block_of_comments.clear()

    #...........................................................................
    def parse__empty_line(self):
        """
                PyParser.parse__empty_line()
                ________________________________________________________________

                A member of the parse__* functions (see general indications
                above).

                Function called when the parser reads an empty line.
        """
        MSG.debug("PyParser.parse__empty_line()")
        self.state.current_block_of_comments.clear()
        self.state.current_class = None

    #...........................................................................
    def parse__sharp_line(self):
        """
                PyParser.parse__sharp_line()
                ________________________________________________________________

                A member of the parse__* functions (see general indications
                above).

                Function called when the parser reads a ligne beginning with '#'.
        """
        MSG.debug("PyParser.parse__sharp_line()")
        line = self.current_liaf.line[1:]
        line = line.strip()

        if len(line) > 0:
            self.state.current_block_of_comments.append(line)

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                PyParser.reset()
                ________________________________________________________________

                Reset the attributes specific to a file.
                ________________________________________________________________

                PARAMETER(S) :  no parameter

                RETURN VALUE :  no return value
        """
        MSG.debug("PyParser.reset()")
        self.current_liaf = LIAF()
        self.state = PyParserState()

    #///////////////////////////////////////////////////////////////////////////
    @staticmethod
    def usefull_comment_line(_line):
        """
                PyParser.usefull_comment_line()
                ________________________________________________________________

                Return True if _line is a usefull line of comment.
                ________________________________________________________________

                PARAMETER :
                    o _line : (str)

                RETURN VALUE : the expected boolean
        """
        return re.match(settings.REGEX__PYTHON_CHARS_IN_USEFULLCOM, _line)
