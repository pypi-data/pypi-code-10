"""Tests for the processors for django-mailer."""
from django.test import TestCase

from mailer.models import PRIORITY_DEFERRED
from mixer.backend.django import mixer

from ..constants import SERVER_STATUS
from ..processors.django_mailer import deferred_emails


class DeferredEmailsProcessorTestCase(TestCase):
    """Test case for the ``deferred_emails`` django-mailer processor."""
    longMessage = True

    def setUp(self):
        self.normal_messages = mixer.cycle(10).blend('mailer.Message')

    def test_deferred_emails(self):
        self.assertEqual(
            deferred_emails()['status'],
            SERVER_STATUS['OK'],
            msg='Without deferred emails, the status should be OK.'
        )

        mixer.cycle(1).blend('mailer.Message', priority=PRIORITY_DEFERRED)
        self.assertEqual(
            deferred_emails()['status'],
            SERVER_STATUS['WARNING'],
            msg='With 1 deferred email, the status should be WARNING.'
        )

        mixer.cycle(9).blend('mailer.Message', priority=PRIORITY_DEFERRED)
        self.assertEqual(
            deferred_emails()['status'],
            SERVER_STATUS['DANGER'],
            msg='With 10 deferred emails, the status should be DANGER.'
        )
