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
        ❏Eupompos❏ eupompos/parserreport.py
        ________________________________________________________________________

        report object used by the Parse classes.
        ________________________________________________________________________

        o ParserReport class
"""

# something's wrong with the way pylint understands the import statement :
# pylint: disable=import-error

from eupompos.strtools import add_prefix_to_lines, rm_initial_spaces
import eupompos.settings as settings

################################################################################
class ParserReport(object):
    """
        ParserReport class
        ________________________________________________________________________

        Object filled by the Parser methods.
        ________________________________________________________________________

        class attributes : -

        instance attribute(s) : -

            o functions : (dict) (str)functionname -> liaf, (list of str)comments

        class methods :

            o __init__()
            o __repr__()
            o clear()
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
                ParserReport.__init__()
                ________________________________________________________________

                Define the instance attributes.
                ________________________________________________________________

                no PARAMETER, no RETURN VALUE
        """
        self.functions = dict()

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                ParserReport.__repr__()
                ________________________________________________________________

                Straightforward representation of the report.
                ________________________________________________________________

                no PARAMETER

                RETURN VALUE : the expected string
        """
        return self.xrepr(settings.PARSERREPORT__FUNCPOS_MAXLENGTH)

    #///////////////////////////////////////////////////////////////////////////
    def clear(self):
        """
                ParserReport.clear()
                ________________________________________________________________

                Reset the values of self.
                ________________________________________________________________

                no PARAMETER, no RETURN VALUE
        """
        self.functions.clear()

    #///////////////////////////////////////////////////////////////////////////
    def xrepr(self, _funcpos_max_length):
        """
                ParserReport.xrepr()
                ________________________________________________________________

                Straightforward representation of the report.
                ________________________________________________________________

                PARAMETER :
                    o _funcpos_max_length : (int) maximal length of the string
                                            describing the function position
                                            in a file.

                RETURN VALUE : the expected string
        """
        res = ["report :",]

        if len(self.functions) == 0:
            res.append("function(s) : no function !")

        else:
            if len(self.functions) == 1:
                res.append("functions : (read 1 function)")
            else:
                res.append("functions : (read {0} functions)".format(len(self.functions)))

            for function in sorted(self.functions):

                liaf, comments = self.functions[function]

                res.append("")
                res.append("o  {0}".format(function.xrepr(_with_liaf=False)))
                res.append("   defined in {0}.".format(liaf.pos_repr(_funcpos_max_length)))

                if len(comments) > 0:
                    comm = add_prefix_to_lines(rm_initial_spaces(comments),
                                               "       « ")
                    res.append("   \n{0}".format("\n".join(comm)))

        return "\n".join(res)
