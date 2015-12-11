import unittest
from mock import patch
import threading

_LOCAL = threading.local()


class Settings(object):
    def __init__(self, settings):
        for item in settings:
            setattr(self, item[0], item[1])


class BaseTest(unittest.TestCase):
    root_name = None

    def auto_patch(self, to_patch, setup_fn=None):
        patcher = patch(to_patch)
        patched = patcher.start()
        setattr(_LOCAL, to_patch.replace('.', '_'), patched)
        if setup_fn:
            setup_fn(patched)
        self.addCleanup(patcher.stop)
        return patched
