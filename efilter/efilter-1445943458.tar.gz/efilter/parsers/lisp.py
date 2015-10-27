# EFILTER Forensic Query Language
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Lisp-like EFILTER syntax.

This is mostly used in tests, in situations where dotty doesn't make it
obvious what the AST is going to look like, and manually setting up expression
classes is too verbose.
"""

__author__ = "Adam Sindelar <adamsh@google.com>"

from efilter import ast
from efilter import syntax


EXPRESSIONS = {
    "var": ast.Binding,
    "!": ast.Complement,
    "map": ast.Map,
    "any": ast.Any,
    "each": ast.Each,
    "find": ast.Filter,
    "sort": ast.Sort,
    "in": ast.Membership,
    "regex": ast.RegexFilter,
    "|": ast.Union,
    "&": ast.Intersection,
    ">": ast.StrictOrderedSet,
    ">=": ast.PartialOrderedSet,
    "==": ast.Equivalence,
    "+": ast.Sum,
    "-": ast.Difference,
    "*": ast.Product,
    "/": ast.Quotient,
}


class Parser(syntax.Syntax):
    """Parses the lisp expression language into the query AST."""

    @property
    def root(self):
        return self._parse_atom(self.original)

    def _parse_atom(self, atom):
        if isinstance(atom, tuple):
            return self._parse_s_expression(atom)

        return ast.Literal(atom)

    def _parse_s_expression(self, atom):
        car = atom[0]
        cdr = atom[1:]

        # Bindings are a little special.
        if car == "var":
            return ast.Binding(cdr[0])

        return EXPRESSIONS[car](*(self._parse_atom(a) for a in cdr))


syntax.Syntax.register_parser(Parser, shorthand="lisp")
