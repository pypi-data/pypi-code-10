from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test.client import RequestFactory
from django.test import TestCase
from django.contrib.admin import site
from django.apps.registry import apps

from .models import TestVidyo1, TestVidyoMock

from dj_oydiv.models import VidyoAdmin
from dj_oydiv.admin.vidyoadmin import VidyoAdminForm


class _AdminFormTestsBase(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser',
            password='password',
            email='user@example.com'
        )
        rf = RequestFactory()

        self.base_request = rf.post(
            '/',
            {
                'dj_auth_user': str(self.user.pk),
                'portal_user': 'admin',
                'portal_host': 'example.com',
                'portal_prefix': 123,
                'user_proxy': 'proxy1',
                'user_group': 'Default',
                'user_location_tag': 'Default',
                'replay_host': 'example.com',
                'cdr_host': 'example.com',
                'cdr_password': 'This field is required.',
                'cdr_port': '3306',
                'cdr_user': 'admin',
                'portal_password': 'password',
                'confirm_portal_password': 'password',
                'current_admin_password': 'password',
            },
            user=self.user
        )

        self.base_request.user = self.user

    def tearDown(self):
        self.user.delete()

    def test_good_form_validates(self):
        form = VidyoAdminForm(self.base_request.POST)
        self.assertTrue(form.is_valid())


class PasswordChangeFormTests(_AdminFormTestsBase):
    """
    Test the admin form password changes and model setup, etc.
    see ``dj_oydiv.admin.monkeypatch_password_form()`` for overrides.
    """

    def test_base_request_form_valid(self):
        """ensure that we have a base level of sanity"""
        form = VidyoAdminForm(self.base_request.POST)
        self.assertTrue(form.is_valid())

    def test_password_change_form_contrib_auth_update(self):
        """
        We're overriding the standard ``save`` method on the
        ``django.contrib.admin.forms.PasswordChangeForm``, but we want to make sure
        that it is still being called, and properly updating the database.
        """
        pass

    def test_password_change_form_no_commit_ignored(self):
        """
        If ``PasswordChangeForm.save(commit=False)``, then we need to not update all
        the vidyoadmin objects.
        """
        pass

    def test_password_change_form_save_fails_rollback(self):
        """
        If  ``PasswordChangeForm.save()`` fails for any reason, we need to have a safe
        rollback strategy.
        """
        pass


class TestAdminFormValidators(_AdminFormTestsBase):

    def test_base_input_valid(self):
        form = VidyoAdminForm(self.base_request.POST)
        self.assertTrue(form.is_valid())
        form.save()

    def test_ip_input_invalid_ipv4(self):
        self.base_request.POST['portal_host'] = '999.999.999.999'
        form = VidyoAdminForm(self.base_request.POST)
        self.assertFalse(form.is_valid())

    def test_ip_input_valid_ipv4(self):
        self.base_request.POST['portal_host'] = '192.168.1.100'
        form = VidyoAdminForm(self.base_request.POST)
        self.assertTrue(form.is_valid())

    def test_ip_input_invalid_ipv6(self):
        self.base_request.POST['portal_host'] = 'xxxx::'
        form = VidyoAdminForm(self.base_request.POST)
        self.assertFalse(form.is_valid())

    def test_hostname_input_accept_hostname_only(self):
        """
        People have a tendency to conflate ``hostname`` with a full uri.
        Here we assert that anything but a hostname causes validation failure.
        """
        self.base_request.POST['portal_host'] = 'https://example.com'
        form = VidyoAdminForm(self.base_request.POST)
        self.assertFalse(form.is_valid())

    def test_domain_invalid_domain(self):
        self.base_request.POST['portal_host'] = 128 * 'a'
        form = VidyoAdminForm(self.base_request.POST)
        self.assertFalse(form.is_valid())

    def test_save_request_without_password_validation_error(self):
        del self.base_request.POST['portal_password']
        with self.assertRaises(ValueError):
            form = VidyoAdminForm(self.base_request.POST)
            form.save()

    def test_request_without_password_is_invalid(self):
        del self.base_request.POST['portal_password']
        form = VidyoAdminForm(self.base_request.POST)
        self.assertFalse(form.is_valid())


class VidyoUserGenericFinderTests(TestCase):
    """
    The admin dicoverer is supposed to find all instances of VidyoUserBase and register them
    with the django admin.
    """
    def test_admin_registry(self):
        self.assertIn(VidyoAdmin, site._registry)

    def test_vidyouserbase_registry(self):
        self.assertIn(TestVidyoMock, apps.get_models())
        self.assertIn(TestVidyo1, apps.get_models())
