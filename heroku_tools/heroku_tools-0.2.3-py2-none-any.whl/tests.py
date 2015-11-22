# -*- coding: utf-8 -*-
import json
import unittest

from mock import patch, call

from heroku_tools.heroku import HerokuRelease, HerokuError, call_api


class MockResponse(object):
    """Mock requests library response.json()."""
    def json(self):
        """Return JSON representation."""
        return json.load(open('heroku_tools/test_data/foo.json', 'r'))

    @property
    def status_code(self):
      return 200


def mock_get(*args, **kwargs):
    return MockResponse()


class HerokuReleaseTests(unittest.TestCase):

    def setUp(self):
        self.json_input = {'app': {'name': 'hulahoop'}}
        self.herokurelease = HerokuRelease(self.json_input)
        self.foo = MockResponse().json()

    @patch("heroku_tools.heroku.call_api")
    @patch("heroku_tools.heroku.click.echo")
    @patch("heroku_tools.heroku.HerokuRelease")
    def test_get_latest_deployment(self, HerokuRelease, echo, call_api):
        """Test unpacking of Heroku API release JSON."""
        call_api.return_value = [
            {'description': 'Deploy'},
            {'description': 'Promote'}
        ]
        self.herokurelease.get_latest_deployment('x')
        self.assertEqual(
            HerokuRelease.call_args,
            call({'description': 'Deploy'})
        )

        #  If no Deploy or Promote description HerokuError will be raised
        call_api.return_value = [{'description': 'Hulahoop'}]
        with self.assertRaises(HerokuError):
            self.herokurelease.get_latest_deployment('x')
            print echo.call_args

    @patch("requests.auth.HTTPBasicAuth")
    @patch("requests.get", side_effect=mock_get)
    def test_call_api(self, get, HTTPBasicAuth):

        """Test call_api function of heroku_tools"""

        HTTPBasicAuth.return_value = "authorized"
        result = call_api('endpoint-%s', 'application', 'range_header')
        self.assertEqual(
            get.call_args,
            call(
                'endpoint-application',
                auth='authorized',
                headers={
                    'Range': 'range_header',
                    'Accept': 'application/vnd.heroku+json; version=3'
                }
            )
        )
        self.assertEqual(result, self.foo)