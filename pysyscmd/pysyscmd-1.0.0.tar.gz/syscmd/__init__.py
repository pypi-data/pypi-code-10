# -*- coding: utf-8 -*-

__author__ = 'Steven Willis'
__email__ = 'onlynone@gmail.com'
__version__ = '1.0.0'

import subprocess

__all__ = ["CALL", "CHECK_CALL", "CHECK_OUTPUT"]

CALL = 'call'
CHECK_CALL = 'check_call'
CHECK_OUTPUT = 'check_output'

_sub_calls = {
    CALL: subprocess.call,
    CHECK_CALL: subprocess.check_call,
    CHECK_OUTPUT: subprocess.check_output
}

_default_subprocess_kwargs = {
    'close_fds': True,
    'shell': False,
}

del subprocess
