"""Tests for the views of the ``server_guardian`` app."""
from django.test import TestCase

from mixer.backend.django import mixer
from django_libs.tests.mixins import ViewRequestFactoryTestMixin

from .. import views


class GuardianDashboardViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``GuardianDashboardView`` view class."""
    view_class = views.GuardianDashboardView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.admin = mixer.blend('auth.User', is_superuser=True)

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.admin)
        self.redirects(user=self.user, to='{0}?next={1}'.format(
            self.get_login_url(), self.get_url()))
