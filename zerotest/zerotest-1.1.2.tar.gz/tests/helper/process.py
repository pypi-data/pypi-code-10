import subprocess
import shlex

from tests import DEBUG


def call_process(cmd):
    try:
        from subprocess import DEVNULL
    except ImportError:
        import os
        DEVNULL = open(os.devnull, 'wb')
    if DEBUG:
        out = None
        close_fds = False
    else:
        out = DEVNULL
        close_fds = True

    args = shlex.split(cmd)
    return subprocess.call(args, stdout=out, stderr=out, close_fds=close_fds)
