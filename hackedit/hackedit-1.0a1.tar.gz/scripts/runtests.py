"""
This script run our test suite.

YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/check_api_coverage.py
"""
import os
import sys


os.system('%s setup.py  test' % sys.executable)
