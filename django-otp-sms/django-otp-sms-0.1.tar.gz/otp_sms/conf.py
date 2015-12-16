# -*- coding: utf-8 -*-
from datetime import timedelta
import django.conf


class Settings(object):
    _defaults = {
        'OTP_SMS_SESSION_KEY_DEVICE_ID': 'OTP-DEVICE-ID',
        'OTP_SMS_SESSION_KEY_LAST_ATTEMPT_TIME': 'OTP-LAST-TIME',
        'OTP_SMS_SESSION_KEY_ATTEMPT': 'OTP-ATTEMPT',
        'OTP_SMS_COUNT_ATTEMPTS': 3,
        'OTP_SMS_LATENCY_ATTEMPTS': timedelta(minutes=5),
        'OTP_SMS_AUTH': None,
        'OTP_SMS_CHALLENGE_MESSAGE': u"Sent by SMS",
        'OTP_SMS_FROM': None,
        'OTP_SMS_TOKEN_TEMPLATE': '{token}',
        'OTP_SMS_TOKEN_VALIDITY': 30,
        'OTP_SMS_TEST_NUMBER': '+79000000000',
        'OTP_SMS_ADAPTER': 'otp_sms.adapters.ConsoleAdapter'
    }

    def __getattr__(self, name):
        if hasattr(django.conf.settings, name):
            value = getattr(django.conf.settings, name)
        elif name in self._defaults:
            value = self._defaults[name]
        else:
            raise AttributeError(name)

        return value


settings = Settings()