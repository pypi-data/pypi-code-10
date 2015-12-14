#!/usr/bin/env python

from sinope.solver_test import *
from tst.tst_test import *
import unittest
from sinope.utilities import *
import doctest

if __name__=="__main__":
	unittest.main(verbosity=2, exit=False)
	(failures, tests) = doctest.testmod(report=True)
	if failures==0: print "Doctest: OK"
