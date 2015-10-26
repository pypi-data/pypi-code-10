"""

"""
import os
import tempfile
import unittest


import jiracli
from jiracli.bridge import JiraSoapBridge
from jiracli.utils import Config
from .common_bridge_cases import BridgeTests, jiravcr


class SoapBridgeTests(unittest.TestCase, BridgeTests):
    def setUp(self):
        tmp_config = tempfile.mktemp()
        self.config = Config(tmp_config)
        jiracli.utils.CONFIG_FILE = tmp_config
        self.cache_dir = tempfile.mkdtemp()
        jiracli.cache.CACHE_DIR = self.cache_dir
        self.config.username = "testuser"
        self.config.password = "testpassword"
        self.vcr_directory = "fixtures/soap"
        with jiravcr.use_cassette(os.path.join(self.vcr_directory, "login.yaml")):
            self.bridge = JiraSoapBridge("https://indydevs.atlassian.net",
                                         self.config)
            self.bridge.login(self.config.username, self.config.password)
