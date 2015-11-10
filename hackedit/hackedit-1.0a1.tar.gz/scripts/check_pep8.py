"""
Checks PEP8 compliance.

Requires pytest-pep8.

YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/check_pep8.py
"""
import os
import sys


os.system('%s setup.py test -a "--pep8 -m pep8"' % sys.executable)
