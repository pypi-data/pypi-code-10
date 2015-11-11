# coding: utf-8
from django import forms
from django.utils.translation import ugettext as _

from django_briteverify.api import check_email

__ALL__ = ('BriteverifyFormMixin',)


class BriteverifyFormMixin(object):
    EMAIL_FIELD_NAME = 'email'

    error_messages = {
        'invalid_email': _('This is an invalid email address. '
                           'Maybe you mistyped?'),
        'disposable_email': _('Please provide your real email address.')
    }

    def clean(self):
        super(BriteverifyFormMixin, self).clean()

        email = self.cleaned_data.get(self.EMAIL_FIELD_NAME)

        # If we already have errors - not making request to service
        if not email or self.errors:
            return

        email_status = check_email(email)

        if not email_status['valid']:
            self.add_error(self.EMAIL_FIELD_NAME,
                           self.error_messages['invalid_email'])
            return

        if email_status['disposable']:
            self.add_error(self.EMAIL_FIELD_NAME,
                           self.error_messages['disposable_email'])
            return

    def add_error(self, field, message, *args, **kwargs):
        parent = super(BriteverifyFormMixin, self)

        # Django >= 1.7
        if hasattr(parent, 'add_error'):
            return parent.add_error(field, message, *args, **kwargs)

        self._errors[field] = [message]
        return
