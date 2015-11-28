from __future__ import absolute_import, unicode_literals

import six

from django.test import TestCase

from .models import (
    TestVidyo1,
    VidyoAdmin,
)
from dj_oydiv.models import IPModel


class TestVidyoObjectDunderStr(TestCase):
    """
    All the Vidyo models have overridden ``__str__()`` methods. These testcases
    are just here for py2/py3 compatibility checks
    """
    def test_vidyoadmin_str(self):
        admin = VidyoAdmin()
        self.assertIn('VidyoAdmin', six.text_type(admin))
        self.assertIn('VidyoAdmin', str(admin))

    def test_vidyo_user_str(self):
        user = TestVidyo1(_admin_model=VidyoAdmin())
        self.assertIn('TestVidyo1', six.text_type(user))
        self.assertIn('TestVidyo1', str(user))

    def test_ipmodel_str(self):
        ip = IPModel(ip='[100::]')
        self.assertIn('[100::]', six.text_type(ip))
        self.assertIn('[100::]', str(ip))
