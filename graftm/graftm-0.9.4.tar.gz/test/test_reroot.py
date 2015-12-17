#!/usr/bin/env python

#=======================================================================
# Authors: Ben Woodcroft, Joel Boyd
#
# Unit tests.
#
# Copyright
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.
#=======================================================================


import unittest
import os.path
import sys

from skbio.tree import TreeNode
from graftm.rerooter import Rerooter

sys.path = [os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')]+sys.path

class Tests(unittest.TestCase):
    
    def test_reroot_trifurcated_tree_at_longest_child(self):
        test_tree_1 ='(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);'
        test_tree_2 ="((B:0.2,(C:0.3,D:0.4):0.1):0.25,A:0.25)root:0;"
        test_tree_3 ='(A:0.1,B:0.5,(C:0.3,D:0.4):0.1);'

        expected_tree_1 = "((A:0.1,B:0.2):0.25,(C:0.3,D:0.4):0.25)root:0;"
        Rerooter().reroot(test_tree)


if __name__ == "__main__":
    unittest.main()
