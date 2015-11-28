# -*- coding: utf-8 -*-

from django.test import TestCase

from dj_oydiv.config import config


class DefaultConfigTests(TestCase):
    def test_overrides(self):
        """Ensure that settings are overriden in the config
        object when the user has defined the corresponding variable in
        settings.py
        """
        orig = config.DEFAULT_PROXY_NAME
        newsetting = orig * 2
        with self.settings(OYDIV_DEFAULT_PROXY_NAME=newsetting):
            self.assertEqual(config.DEFAULT_PROXY_NAME, newsetting)
