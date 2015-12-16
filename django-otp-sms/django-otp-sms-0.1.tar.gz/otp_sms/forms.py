# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField
from .models import SMSDevice
from .conf import settings


class OTPSMSAuthenticationFormMixin(object):

    def clean_otp(self, username):
        if username:
            device = self._get_device(username)
            self._handle_challenge(device)

    def _get_device(self, phone):
        now = datetime.now()
        attempt = self.request.session.get(settings.OTP_SMS_SESSION_KEY_ATTEMPT, 0)
        last_attempt_time = self.request.session.get(settings.OTP_SMS_SESSION_KEY_LAST_ATTEMPT_TIME)
        if last_attempt_time:
            try:
                last_attempt_time = datetime.fromtimestamp(last_attempt_time)
            except:
                last_attempt_time = None

        if attempt:
            try:
                attempt = int(attempt)
            except:
                attempt = 0

        if settings.OTP_SMS_COUNT_ATTEMPTS and attempt >= settings.OTP_SMS_COUNT_ATTEMPTS:
            if last_attempt_time and now - last_attempt_time < settings.OTP_SMS_LATENCY_ATTEMPTS:
                raise forms.ValidationError(u'Вы превысили лимит sms попробуйте через %d минут' % (settings.OTP_SMS_LATENCY_ATTEMPTS.total_seconds() / 60,))
            else:
                attempt = 0

        device = SMSDevice.objects.create(number=phone)
        self.request.session[settings.OTP_SMS_SESSION_KEY_DEVICE_ID] = device.pk
        self.request.session[settings.OTP_SMS_SESSION_KEY_LAST_ATTEMPT_TIME] = time.mktime(datetime.now().timetuple())
        self.request.session[settings.OTP_SMS_SESSION_KEY_ATTEMPT] = attempt + 1

        return device

    def _handle_challenge(self, device):
        try:
            challenge = device.generate_challenge() if (device is not None) else None
        except Exception as e:
            raise forms.ValidationError('Error generating challenge: {0}'.format(e))
        else:
            if challenge is None:
                raise forms.ValidationError('Error generating challenge')


class OTPSMSAuthenticationForm(AuthenticationForm, OTPSMSAuthenticationFormMixin):
    username = PhoneNumberField()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(number=username, token=password, request=self.request)
            if self.user_cache is None:
                raise forms.ValidationError(
                    u'Код подтверждения введен неверно'
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        elif username and self.user_cache is None:
            self.clean_otp(username)

        return self.cleaned_data