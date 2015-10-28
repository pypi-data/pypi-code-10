# -*- coding: utf-8 -*-
"""
Tests for the subscribers app.
"""
from __future__ import unicode_literals
from django.contrib.auth.models import User, Permission
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch
from holding_page.subscribers.forms import SubscriberForm, UnsubscribeForm
from holding_page.subscribers.models import Subscriber


class SubscriptionFormTestCase(TestCase):
    """
    Collection of tests to ensure the subscription form works correctly
    """
    fixtures = ['test_data.json']

    def setUp(self):
        self.data = {
            'full_name': 'Test Name',
            'email': 'test@example.com'
        }

    def test_subscriber_model_has_unicode(self):
        """
        Tests that subscribers have a unicode display for the admin.
        """
        subscriber = Subscriber(email='test@example.com', full_name='Full Name')
        self.assertEquals(subscriber.__unicode__(), 'Full Name <test@example.com>')

    def test_form_renders(self):
        """
        Tests that the form renders correctly
        """
        response = self.client.get(reverse('subscriber:subscriber_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], SubscriberForm))

    def test_form_submits(self):
        """
        Tests that the form can be submitted with post, and the Fullname
        and email address are saved
        """
        response = self.client.post(reverse('subscriber:subscriber_form'),
                                    self.data)
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, reverse('subscriber:thank_you'))
        Subscriber.objects.get(email='test@example.com', full_name='Test Name')

    def test_form_unique_email(self):
        """
        Tests that the form requires a unique email address
        """
        self.client.post(reverse('subscriber:subscriber_form'), self.data)
        response = self.client.post(reverse('subscriber:subscriber_form'),
                                    self.data)
        self.assertFormError(response,
                             "form",
                             'email',
                             'Subscriber with this Email address already exists.')

    def test_form_valid_email(self):
        """
        Tests that the form does not save details if the details provided
        are incorrect, i.e. badly formatted email address
        """
        data = {'email': 'test@example'}
        response = self.client.post(reverse('subscriber:subscriber_form'), data)
        self.assertTrue(response.status_code, 200)
        self.assertFormError(response, "form", 'email', 'Enter a valid email address.')

    def test_form_required_fields(self):
        """
        Tests that the form raises errors if required fields are not provided
        """
        data = {}
        response = self.client.post(reverse('subscriber:subscriber_form'), data)
        self.assertTrue(response.status_code, 200)
        self.assertFormError(response,
                             "form",
                             'email',
                             'This field is required.')
        self.assertFormError(response,
                             "form",
                             'full_name',
                             'This field is required.')

    def test_send_email(self):
        """
        Tests that an email is sent to new users, and that the email includes
        their sharing URL
        """
        self.client.post(reverse('subscriber:subscriber_form'), self.data)
        self.assertEqual(len(mail.outbox), 1)

    @patch('holding_page.subscribers.models.uuid4')
    def test_subscription_share_code(self, uuid4):
        """
        Tests that every new user has a share code generated and saved
        """
        uuid4.return_value = '68b475a0-5e1c-4a3a-8eae-db469acd65a6'
        self.client.post(reverse('subscriber:subscriber_form'), self.data)
        subscriber = Subscriber.objects.get(email='test@example.com', full_name='Test Name')
        self.assertEquals(subscriber.share_code, '68b475a0-5e1c-4a3a-8eae-db469acd65a6')

    def test_form_renders_with_share_code(self):
        """
        Tests that a form submitted with a share code correctly saves the
        reference to this share code
        """
        referrer = Subscriber.objects.get(pk=1)
        response = self.client.get(reverse('subscriber:subscriber_form_with_code', args=[referrer.share_code]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['source_share_code'], referrer.share_code)

    def test_form_valid_share_code(self):
        """
        Tests that a share code entered is actually valid, raises an error if not
        """
        self.data['source_share_code'] = '1234567890'
        response = self.client.post(reverse('subscriber:subscriber_form'),
                                    self.data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response,
                             "form",
                             'source_share_code',
                             'Invalid share code.')

    def test_remove_email_address_renders(self):
        """
        Tests that the unsubscribe form renders
        """
        response = self.client.get(reverse('subscriber:unsubscribe_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], UnsubscribeForm))

    def test_remove_email_address(self):
        """
        Tests that posting an email to the unsubscribe remove that user's entry
        """
        data = {'email': 'testdata@example.com'}
        response = self.client.post(reverse('subscriber:unsubscribe_form'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('subscriber:successful_unsubscribe'))

    def test_unsubscribe_form_valid_email_address(self):
        """
        Tests that a share code entered is actually valid, raises an error if not
        """
        self.data['email'] = 'blah@example.com'
        response = self.client.post(reverse('subscriber:unsubscribe_form'), self.data)
        self.assertFormError(response, 'form', 'email', 'Invalid email address.')

    def test_remove_email_address_renders_with_email(self):
        """
        Tests that the unsubscribe form renders with a provided email address
        """
        response = self.client.get(reverse('subscriber:unsubscribe_form_with_email',
                                           args=['testdata@example.com']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['email'], 'testdata@example.com')

    def test_export_data(self):
        """
        Tests that the export data admin view correctly renders a CSV
        """
        staff_user = User.objects.create_superuser(
            username='staff_user',
            email="staff_user@example.com",
            password='staff_user'
        )
        export_csv = Permission.objects.get(codename='export_csv')
        staff_user.user_permissions.add(export_csv)
        staff_user.save()
        self.client.login(username="staff_user", password="staff_user")
        response = self.client.get(reverse('subscriber:export_csv'))
        self.assertEqual(response.content, b'"Test Data User","testdata@example.com","0"\n')
