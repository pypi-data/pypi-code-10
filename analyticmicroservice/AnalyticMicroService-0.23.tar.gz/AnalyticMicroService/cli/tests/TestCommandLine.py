__author__ = 'Chris Bergh'
import sys
if not '../' in sys.path:
    sys.path.insert(0, '../')
import unittest
from nose.tools import nottest
from modules.AMSCommandRunner import AMSCommandRunner
from modules.AMSCommandRunnerConfig import *
import requests
from requests import RequestException


class TestCommandLine(unittest.TestCase):

    _cr_config = AMSCommandRunnerConfig()
    _cr_config_dict = dict()
    
    @nottest
    def clean_containers(self):
        cr =  AMSCommandRunner(self._cr_config)
        cr.force_remove_container()

    def setUp(self):
        print(__name__, ': TestCommandLine.setUp()  - - - - - - - -')
        self._cr_config_dict[AMS_PORT] = '14001'
        self._cr_config_dict[AMS_URL] = 'http://127.0.0.1'
        self._cr_config_dict[AMS_CONTAINER_NAME] = 'analytic_micro_service'
        self._cr_config_dict[AMS_IMAGE_REPO] = 'cbergh/analytic_micro_service'
        self._cr_config_dict[AMD_IMAGE_TAG] = 'base_v1'
        self.assertTrue(self._cr_config.init_from_dict(self._cr_config_dict))
        self.clean_containers()

    def test_images(self):
        cr =  AMSCommandRunner(self._cr_config)
        images = cr.images()
        self.assertIsNotNone(images)

    def test_search(self):
        search_string = 'cbergh'
        cr =  AMSCommandRunner(self._cr_config)
        sr = cr.search(search_string)
        self.assertIsNotNone(sr)

    def test_pull(self):
        cr =  AMSCommandRunner(self._cr_config)
        return_dict = cr.pull()
        self.assertIsNotNone(return_dict)

    def test_start_container(self):
        cr =  AMSCommandRunner(self._cr_config)
        return_dict = cr.pull()
        self.assertIsNotNone(return_dict)
        self.assertTrue(cr.start_container())
        self.assertTrue(cr.stop_container())

    def test_end_to_end_via_request(self):
        port = '14001'
        ip = '127.0.0.1'
        path = 'v1/endtoend'
        cr =  AMSCommandRunner(self._cr_config)
        return_dict = cr.pull()
        self.assertIsNotNone(return_dict)
        self.assertTrue(cr.start_container())
        pdict = dict()
        new_contents = None
        try:
            url = 'http://%s:%s/%s' % (ip, cr.get_host_port(), path)
            r = requests.get(url, params=pdict)
            new_contents = r.json()
        except (RequestException, ValueError), c:
            self.assertTrue(False, 'error: %s' % str(c))
        self.assertIsNotNone(new_contents)
        self.assertTrue(cr.stop_container())

    def tearDown(self):
        print(__name__, ': TestCommandLine.tearDown() - - - - - - -')
        self.clean_containers()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
