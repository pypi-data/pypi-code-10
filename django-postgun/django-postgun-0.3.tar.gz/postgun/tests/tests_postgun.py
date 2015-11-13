import httpretty
import datetime
from django.test import TestCase
from django.test.utils import override_settings
from django.core.mail import send_mail as django_send_mail
from django.core.validators import ValidationError
from django.utils.timezone import utc

from postgun.message import MailGunMessage
from postgun.backends import MailgunAPIError
from postgun.validators import validate_email_mailgun
from postgun import send_mail
from postgun.events import get_events
from postgun.tests import EVENTS_PAGE_ONE, EVENTS_PAGE_TWO, EVENTS_PAGE_THREE, EVENTS_PAGE_ONE_URL, \
    EVENTS_PAGE_TWO_URL, EVENTS_PAGE_THREE_URL, EVENTS_ERROR_URL, EVENTS_ERROR


class MailGunMessageTestCase(TestCase):

    def setUp(self):
        self.subject = 'Happy Birthday'
        self.message = 'Test Message'
        self.from_email = 'james@example.com'
        self.reply_to = ['sales@example.com', ]
        self.recipient_list = ['john@example.com', 'smith@example.com', ]
        self.delivery_time = 'Mon, 28 Sep 2015 18:02:00 GMT'
        self.cc = ['mom@example.com', 'dad@example.com']
        self.bcc = ['evil_twin@example.com']
        self.custom_headers = {'Priority': '5'}
        self.tags = ['birthday', 'reminder', ]
        self.campaign = 'birthday_sale'
        self.dkim, self.track, self.track_clicks, self.track_opens = True, True, True, True
        self.message = MailGunMessage(self.subject, self.message, self.from_email, self.recipient_list,
                                      connection=None, campaign=self.campaign, reply_to=self.reply_to,
                                      delivery_time=self.delivery_time, dkim=self.dkim, track=self.track,
                                      track_clicks=self.track_clicks, track_opens=self.track_opens,
                                      custom_headers=self.custom_headers, cc=self.cc, bcc=self.bcc, tags=self.tags)
        self.options = self.message.mailgun_options

    def _test_key_value(self, key, value):
        self.assertTrue(key in self.options)
        self.assertEqual(self.options[key], value)

    def test_campaign(self):
        self._test_key_value('o:campaign', self.campaign)

    def test_deliverytime(self):
        self._test_key_value('o:deliverytime', self.delivery_time)

    def test_tags(self):
        self._test_key_value('o:tag', self.tags)

    def test_dkim(self):
        self._test_key_value('o:dkim', self.dkim)

    def test_tracking(self):
        self._test_key_value('o:tracking', self.track)

    def test_tracking_clicks(self):
        self._test_key_value('o:tracking-clicks', self.track_clicks)

    def test_tracking_opens(self):
        self._test_key_value('o:tracking-opens', self.track_opens)

    def test_custom_headers(self):
        for key, value in list(self.custom_headers.items()):
            self._test_key_value("h:" + key, value)

    def test_reply_to(self):
        self._test_key_value('h:Reply-To', ['sales@example.com'])


@override_settings(EMAIL_BACKEND='postgun.backends.MailgunEmailBackend',
                   MAILGUN_DOMAIN='example.com',
                   MAILGUN_API_KEY='123')
class SendMailTestCase(TestCase):

    @httpretty.activate
    def test_sends_email(self):
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body='{}', status=200)
        result = send_mail('Test Subject', 'My message', 'admin@example.com', ['james@example.com'], )
        self.assertEqual(1, result)

    @httpretty.activate
    def test_sends_cc_bcc_html_email(self):
        body = u'{\n  "id": "<20151111144935.53694.47080@jamess-macbook-pro.local>",\n  "message": "Queued. Thank you."\n}'
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body=body, status=200)

        response_data = {}
        result = send_mail('Test Subject', 'My message', 'admin@example.com', ['james@sugoisoft.com'],
                           html_message='My <strong>message</strong>', cc=['john@example.com'],
                           bcc=['jacob@example.com'], response_data=response_data)
        self.assertEqual(1, result)
        self.assertNotEqual({}, response_data)
        self.assertEqual(response_data['message'], "Queued. Thank you.")
        self.assertEqual(response_data['id'], u"<20151111144935.53694.47080@jamess-macbook-pro.local>")


    @httpretty.activate
    def test_fails_silently(self):
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body='{}', status=401)
        result = send_mail('Test Subject', 'My message', 'admin@example.com', ['james@example.com'], fail_silently=True)
        self.assertEqual(0, result)

    @httpretty.activate
    def test_rasies_error(self):
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body='{}', status=401)
        self.assertRaises(MailgunAPIError, send_mail, 'Test Subject', 'My message', 'admin@example.com',
                          ['james@example.com'], fail_silently=False)


@override_settings(EMAIL_BACKEND='postgun.backends.MailgunEmailBackend')
class NoSettingsTestCase(TestCase):

    def test_no_settings_noisy(self):
        self.assertRaises(AttributeError, send_mail, 'Test Subject', 'My message', 'admin@example.com',
                          ['james@example.com'], fail_silently=False)

    def test_no_settings_silent(self):
        result = send_mail('Test Subject', 'My message', 'admin@example.com', ['james@example.com'], fail_silently=True)
        self.assertEqual(0, result)


@override_settings(EMAIL_BACKEND='postgun.backends.MailgunEmailBackend',
                   MAILGUN_DOMAIN='example.com',
                   MAILGUN_API_KEY='123')
class DjangoSendMailTestCase(TestCase):

    @httpretty.activate
    def test_sends_email(self):
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body='{}', status=200)
        result = django_send_mail('Test Subject', 'My message', 'admin@example.com', ['james@example.com'], )
        self.assertEqual(1, result)

    @httpretty.activate
    def test_fails_silently(self):
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body='{}', status=401)
        result = django_send_mail('Test Subject', 'My message', 'admin@example.com', ['james@example.com'], fail_silently=True)
        self.assertEqual(0, result)

    @httpretty.activate
    def test_rasies_error(self):
        httpretty.register_uri(httpretty.POST, "https://api.mailgun.net/v3/example.com/messages",
                               body='{}', status=401)
        self.assertRaises(MailgunAPIError,  django_send_mail, 'Test Subject', 'My message', 'admin@example.com',
                          ['james@example.com'], fail_silently=False)


@override_settings(MAILGUN_PUBLIC_KEY='pubkey-my-public-key')
class EmailValidationTestCase(TestCase):

    @httpretty.activate
    def test_valid_email(self):
        response_text = """{
                          "address": "james@hotmail.co.uk",
                          "did_you_mean": null,
                          "is_valid": true,
                          "parts": {
                            "display_name": null,
                            "domain": "hotmail.co.uk",
                            "local_part": "james"
                          }
                        }"""
        httpretty.register_uri(httpretty.GET, "https://api.mailgun.net/v3/address/validate",
                               body=response_text, status=200)
        self.assertTrue(validate_email_mailgun('james@hotmail.co.uk'))

    @httpretty.activate
    def test_invalid_email(self):
        response_text = """{
                          "address": "james@example.co",
                          "did_you_mean": null,
                          "is_valid": false,
                          "parts": {
                            "display_name": null,
                            "domain": null,
                            "local_part": null
                          }
                        }"""
        httpretty.register_uri(httpretty.GET, "https://api.mailgun.net/v3/address/validate",
                               body=response_text, status=200)
        self.assertRaises(ValidationError, validate_email_mailgun, 'james@example.co')

    @httpretty.activate
    def test_did_you_mean(self):
        response_text = """{
                      "address": "james@hotmail.co.u",
                      "did_you_mean": "james@hotmail.co.uk",
                      "is_valid": false,
                      "parts": {
                        "display_name": null,
                        "domain": null,
                        "local_part": null
                      }
                    }"""
        httpretty.register_uri(httpretty.GET, "https://api.mailgun.net/v3/address/validate",
                               body=response_text, status=200)
        self.assertRaises(ValidationError, validate_email_mailgun, 'james@hotmail.co.u')


@override_settings(EMAIL_BACKEND='postgun.backends.MailgunEmailBackend',
                   MAILGUN_DOMAIN='example.com',
                   MAILGUN_API_KEY='123')
class GetEventsTest(TestCase):

    @httpretty.activate
    def test_paginates(self):
        httpretty.register_uri(httpretty.GET, EVENTS_PAGE_ONE_URL, body=EVENTS_PAGE_ONE, status=200)
        httpretty.register_uri(httpretty.GET, EVENTS_PAGE_TWO_URL, body=EVENTS_PAGE_TWO, status=200)
        httpretty.register_uri(httpretty.GET, EVENTS_PAGE_THREE_URL, body=EVENTS_PAGE_THREE, status=200)

        begin = datetime.datetime(year=2015, month=11, day=06, hour=15, minute=11, second=23, tzinfo=utc)
        events = get_events(begin=begin, limit=1)

        self.assertEqual(2, len(events))

    @httpretty.activate
    def test_raises(self):
        httpretty.register_uri(httpretty.GET, EVENTS_ERROR_URL, body=EVENTS_ERROR, status=500)
        begin = datetime.datetime(year=2015, month=11, day=13, hour=15, minute=11, second=49)
        self.assertRaises(MailgunAPIError, get_events, begin=begin, end=begin, limit=1)
