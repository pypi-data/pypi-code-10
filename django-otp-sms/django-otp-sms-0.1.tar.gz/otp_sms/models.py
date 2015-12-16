# -*- coding: utf-8 -*-
import time
from datetime import datetime
from binascii import unhexlify
from django.db import models
from django.utils import timezone
from django.utils.module_loading import import_string
from django_otp.oath import TOTP
from django_otp.util import random_hex, hex_validator
from phonenumber_field.modelfields import PhoneNumberField
from .adapters import AdapterError
from .conf import settings


def default_key():
    return random_hex(20)


def key_validator(value):
    return hex_validator(20)(value)


class SMSDevice(models.Model):
    number = PhoneNumberField(
        help_text="The mobile number to deliver tokens to."
    )

    key = models.CharField(
        max_length=40,
        validators=[key_validator],
        default=default_key,
        help_text="A random key used to generate tokens (hex-encoded)."
    )

    last_t = models.BigIntegerField(
        default=-1,
        help_text="The t value of the latest verified token. The next token must be at a higher time step."
    )

    class Meta(object):
        verbose_name = "SMS Device"

    def __unicode__(self):
        return u'%s' % self.number

    @staticmethod
    def get(request, number):
        device_id = request.session.get(settings.OTP_SMS_SESSION_KEY_DEVICE_ID)
        device = None
        if device_id:
            try:
                device_id = int(device_id)
            except:
                device_id = None
            try:
                device = SMSDevice.objects.get(pk=device_id, number=number)
            except SMSDevice.DoesNotExist:
                pass
        return device

    @property
    def bin_key(self):
        return unhexlify(self.key.encode())

    def generate_challenge(self):
        """
        Sends the current TOTP token to ``self.number``.

        :returns: :setting:`OTP_SMS_CHALLENGE_MESSAGE` on success.
        :raises: Exception if delivery fails.

        """
        totp = self.totp_obj()
        token = format(totp.token(), '06d')
        message = settings.OTP_SMS_TOKEN_TEMPLATE.format(token=token)
        challenge = settings.OTP_SMS_CHALLENGE_MESSAGE.format(token=token)
        self._deliver_token(message)

        return challenge

    def _deliver_token(self, token):
        adapter_klass = import_string(settings.OTP_SMS_ADAPTER)
        adapter = adapter_klass(settings.OTP_SMS_AUTH)
        try:
            adapter.send(self.number, token, sender=settings.OTP_SMS_FROM)
        except AdapterError as e:
            if settings.DEBUG:
                raise e

    def verify_token(self, token):
        try:
            token = int(token)
        except Exception:
            verified = False
        else:
            totp = self.totp_obj()
            tolerance = settings.OTP_SMS_TOKEN_VALIDITY

            for offset in range(-tolerance, 1):
                totp.drift = offset
                if (totp.t() > self.last_t) and (totp.token() == token):
                    self.last_t = totp.t()
                    self.save()

                    verified = True
                    break
            else:
                verified = False

        return verified

    def totp_obj(self):
        totp = TOTP(self.bin_key, step=1)
        totp.time = time.time()

        return totp