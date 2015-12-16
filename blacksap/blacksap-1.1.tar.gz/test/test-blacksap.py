#!/usr/bin/env python
# coding=utf-8
"""Unittests for blacksap.  This tests both the cli interface and internal functions for blacksap.
"""
from __future__ import print_function
import unittest
import time
import os
import shutil
from click.testing import CliRunner
import blacksap
__author__ = 'Jesse Almanrode (jesse@almanrode.com)'


class TestBlacksap(unittest.TestCase):

    def test_help(self):
        """ Make sure there aren't any parse errors
        :return: exit_code == 0
        """
        runner = CliRunner()
        result = runner.invoke(blacksap.cli, ['--help'])
        assert result.exit_code == 0
        pass

    def test_tracking(self):
        """ Test tracking command
        :return: exit_code == 0 and 'feeds tracked' in output
        """
        runner = CliRunner()
        result = runner.invoke(blacksap.cli, ['tracking'])
        assert result.exit_code == 0
        assert 'feeds tracked' in result.output
        pass

    def test_track_valid(self):
        """ Test track command for a valid URL/Feed
        :return: exit_code == 0
        """
        runner = CliRunner()
        result = runner.invoke(blacksap.cli, ['track', 'http://kat.cr/usearch/yify%201080p/?rss=1'])
        assert result.exit_code == 0
        pass

    def test_track_invalid(self):
        """ Test track command for invalid URL/Feed
        :return: exit_code == 1
        """
        runner = CliRunner()
        result = runner.invoke(blacksap.cli, ['track', 'http://jacomputing.net/'])
        assert result.exit_code != 0
        pass

    def test_untrack_valid(self):
        """ Test untrack command for valid URL/Feed
        :return: exit_code == 0
        """
        runner = CliRunner()
        result = runner.invoke(blacksap.cli, ['untrack', 'http://kat.cr/usearch/yify%201080p/?rss=1'])
        assert result.exit_code == 0
        pass

    def test_untrack_invalid(self):
        """ Test untrack command for invalid URL/Feed
        :return: exit_code == 0
        """
        runner = CliRunner()
        result = runner.invoke(blacksap.cli, ['untrack', 'http://jacomputing.net/'])
        assert result.exit_code == 0
        pass

    def test_run(self):
        """ Test run command
        :return:
        """
        runner = CliRunner()
        self.test_track_valid()
        os.mkdir('/tmp/blacksap_test/')
        result = runner.invoke(blacksap.cli, ['run', '--count', '1', '--force', '-o', '/tmp/blacksap_test/'])
        shutil.rmtree('/tmp/blacksap_test/')
        self.test_untrack_valid()
        assert result.exit_code == 0
        assert 'RSS feeds checked in:' in result.output
        pass

    def test_clearcache(self):
        """ Test clearcache command
        :return:
        """
        pass

    def test_read_cfg(self):
        """ Test read_cfg method
        :return: Dictionary
        """
        result = blacksap.read_cfg()
        assert isinstance(result, dict)
        pass

    def test_writecfg(self):
        """ Test write_cfg method
        :return: True
        """
        cfg = blacksap.read_cfg()
        result = blacksap.write_cfg(cfg)
        assert result is True
        pass

    def test_ttl_expired(self):
        """ Test ttl_expired method
        :return: True and False
        """
        now = time.time()
        result = blacksap.ttl_expired(now, 600)
        assert result is False
        now -= 610
        result = blacksap.ttl_expired(now, 600)
        assert result is True
        pass

    def test_download_torrent_file(self):
        """ Test whether or not we can curl a url
        :return: True and False
        """
        result = blacksap.download_torrent_file('not_a_valid_url', '/tmp/', 'blacksap.test', 1)
        assert result[0] is False
        result = blacksap.download_torrent_file('http://jacomputing.net/myip/', '/tmp/', 'blacksap.test', 1)
        assert result[0] is True
        os.remove('/tmp/blacksap.test')
        pass


if __name__ == '__main__':
    blacksap.__config__ = '/tmp/blacksap.cfg'
    unittest.main()
    os.remove('/tmp/blacksap.cfg')
