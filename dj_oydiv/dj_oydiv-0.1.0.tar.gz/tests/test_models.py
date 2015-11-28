from __future__ import absolute_import, unicode_literals

import mock

from django.test import TestCase, SimpleTestCase

from . import PACKAGE_BASE, VIDYO_PORTAL_PASSWORD
from .models import (
    TestVidyoMock,
    TestVidyo1,
    create_test_admin,
    create_multiple_children,
)

from dj_oydiv.models import VidyoUserBase, VidyoAdmin
from dj_oydiv.utils.random import random_ascii_letters


"""
Factory function tests.
The factory functions defined in the factory module are expected to return a
``django.model.Model`` or VUser/VReplay/VCDRInfo object depending on the function.
Most take a client ID and a class type, and retrieve the appropriate model.

Multiple objects should *never* be returned.
"""


class AdminWithMultipleChildrenMixin(object):
    N_CHILD_USERS = 8

    def setUp(self):
        self.admin = create_test_admin()

        # now create and save a bunch of derivatives of VidyoUserBase
        self.test0_users = [(x + 1) * 'b' for x in range(self.N_CHILD_USERS)]
        create_multiple_children(self.admin, self.test0_users, TestVidyoMock, self.N_CHILD_USERS)

        self.test1_users = [(x + 1) * 'a' for x in range(self.N_CHILD_USERS)]
        create_multiple_children(self.admin, self.test1_users, TestVidyo1, self.N_CHILD_USERS)

    def tearDown(self):
        TestVidyoMock.objects.all().delete()


class VidyoAdminMethodTests(AdminWithMultipleChildrenMixin, TestCase):
    def test_password_change_propagates_children(self):
        self.admin.change_key(VIDYO_PORTAL_PASSWORD, 'mynewpassword')
        self.admin.save()
        for x in list(TestVidyoMock.objects.all()) + list(TestVidyo1.objects.all()):
            with self.assertRaises(ValueError):
                x.decrypt('mypassword')

            x.decrypt('mynewpassword')
            self.assertEqual(x.password, 'mysecretdata')

    def test_all_vidyo_user_classes_complete(self):
        for x in [TestVidyoMock, TestVidyo1]:
            if x not in VidyoUserBase.all_vidyo_user_classes():
                raise Exception("Non-abstract models not registered")

    def test_all_vidyo_users_complete(self):
        """make sure the expected number of TestVidyoMock/TestVidyo1 children are listed"""
        self.assertEqual(self.N_CHILD_USERS * 2, len(list(self.admin.all_vidyo_users())))

    def test_all_vidyo_users_match_admin(self):
        """
        Make sure that the ``a.all_vidyo_users``method does not return any objects in
        ``b.all_vidyo_users()``
        """
        a = create_test_admin(admin='donny')
        # We must compare lists, rather than iterators
        self.assertNotEqual(
            sorted(list(a.all_vidyo_users()), key=lambda x: x.pk),
            sorted(list(self.admin.all_vidyo_users()), key=lambda x: x.pk)
        )
        self.assertEqual(len(list(a.all_vidyo_users())), 0)

    def test_all_vidyo_users_objects(self):
        for x in self.test0_users:
            u = TestVidyoMock.objects.get(client_id=x)
            self.assertIn(u, self.admin.all_vidyo_users())
        for x in self.test1_users:
            u = TestVidyo1.objects.get(client_id=x)
            self.assertIn(u, self.admin.all_vidyo_users())

    def test_ssl_propagation(self):
        """
        assert that the value returned by admin.use_ssl() is equal to admin.ssl
        among all related VidyoAdmin/VidyoUserBase objects.
        """
        self.admin.ssl = True
        self.admin.save()
        self.assertTrue(self.admin.use_ssl())
        for x in self.admin.all_vidyo_users():
            self.assertTrue(x.use_ssl())
        self.admin.ssl = False
        self.admin.save()
        self.assertFalse(self.admin.use_ssl())
        for x in self.admin.all_vidyo_users():
            self.assertFalse(x.use_ssl())

    def test_user_count(self):
        self.assertEqual(self.N_CHILD_USERS * 2, self.admin.user_count)

    def test_user_count_multiple_admins(self):
        a = create_test_admin(admin='donny')
        self.assertFalse(a.user_count, 0)
        self.assertEqual(self.N_CHILD_USERS * 2, self.admin.user_count)


class ModelDefaultsTests(SimpleTestCase):
    def test_bare_save_new_password(self):
        """
        just calling save should be enough to generate a random password
        on a user model
        """
        with mock.patch(
            PACKAGE_BASE + '.utils.random.get_random_string',
            mock.Mock(return_value='thisisrandom')
        ):
            ad = VidyoAdmin()
            ad.secret_key = 'pizzatime'
            ad.password = 'whatever'
            ad.save()

            model = TestVidyoMock(_admin_model=ad)
            model.secret_key = 'pizzatime'
            model.save()
            self.assertEqual(model.password, 'thisisrandom')

    def test_new_model_pin_not_equal(self):
        alice = TestVidyoMock(_admin_model=VidyoAdmin())
        bob = TestVidyoMock(_admin_model=VidyoAdmin())
        self.assertNotEqual(bob.pin, alice.pin)
