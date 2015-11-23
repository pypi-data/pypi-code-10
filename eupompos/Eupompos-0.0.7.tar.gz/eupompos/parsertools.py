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
        ❏Eupompos❏ eupompos/parsertools.py

        o FunctionName class
"""

################################################################################
class FunctionName(object):
    """
        FunctionName class
        ________________________________________________________________________

        Use this class to read/write informations about a function/method name
        ________________________________________________________________________

        class attributes : -

        instance attributes :

            o classname : (str)
            o functioname : (str)

        methods :

            o __init__()
            o __repr__()
            o init_from_str()
            o xrepr()
    """
    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, _classname=None, _functionname=""):
        """
                FunctionName.__init__()
                ________________________________________________________________

                Create the attributes.
                ________________________________________________________________

                PARAMETERS :
                    o _classname : None/str
                    o _functionname : (str)

                RETURN VALUE : no return value
        """
        self.classname = _classname
        self.functionname = _functionname

    #///////////////////////////////////////////////////////////////////////////
    def __lt__(self, _other):
        """
                FunctionName.__lt__()
                ________________________________________________________________

                Return True if self < _other
                ________________________________________________________________

                PARAMETER :
                    o _other : another FunctionName object

                RETURN VALUE : the expected boolean
        """
        if self.classname is None and _other.classname is None:
            return self.functionname < _other.functionname

        if self.classname is None and _other.classname is not None:
            return True

        if self.classname is not None and _other.classname is None:
            return False

        # last case : we have (self.classname, _other.classname) different from None.
        if self.classname == _other.classname:
            return self.functionname < _other.functionname

        return self.classname < _other.classname

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                FunctionName.__repr__()
                ________________________________________________________________

                Return a string representation of self.
                ________________________________________________________________

                no PARAMETER

                RETURN VALUE : the expected string
        """
        return self.xrepr()

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, _str, _language):
        """
                FunctionName.__repr__()
                ________________________________________________________________

                Return a string representation of self.
                ________________________________________________________________

                PARAMETERS :
                    _str      : source string
                    _language : (str) "cpp" or "python"

                RETURN VALUE : return self
        """
        if _language == "cpp":
            if "::" in _str:
                self.classname = _str[:_str.find("::")]
                self.functionname = _str[_str.find("::")+2:]
            else:
                self.classname = None
                self.functionname = _str

        return self

    #///////////////////////////////////////////////////////////////////////////
    def xrepr(self):
        """
                FunctionName.xrepr()
                ________________________________________________________________

                Return a string representation of self.
                ________________________________________________________________

                no PARAMETER

                RETURN VALUE : the expected string
        """
        if self.classname is not None:
            return "{0}::{1}()".format(self.classname,
                                       self.functionname)
        else:
            return "{0}".format(self.functionname)
