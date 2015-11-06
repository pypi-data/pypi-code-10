'''
Loads all tests in module and run
'''
import doctest
import sys
import FGAme as mod_current
from FGAme import conf  # @Reimport
conf.set_backend('empty')
from FGAme.tests.all import *  # @UnusedWildImport
print('Starting tests using backend: %s' % conf.get_backend())

from pytest import main
main('-v --doctest-modules')
