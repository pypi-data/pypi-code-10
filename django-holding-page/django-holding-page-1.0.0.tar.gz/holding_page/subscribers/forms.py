# -*- coding: utf-8 -*-
"""
Forms used to create subscribers and allow them to unsubscribe.
"""
from holding_page.subscribers.models import Subscriber
from django import forms
from django.utils.translation import ugettext as _


class SubscriberForm(forms.ModelForm):
    """
    Forms used to create a subscriber.
    """
    class Meta(object):
        model = Subscriber
        fields = ['full_name', 'email', 'source_share_code']
        widgets = {
            'source_share_code': forms.HiddenInput(),
        }

    def clean_source_share_code(self):
        """
        Looks for the share code and raises a validation error if it is not valid.
        """
        if self.cleaned_data['source_share_code'] != '':
            if not Subscriber.objects.filter(share_code=self.cleaned_data['source_share_code']).exists():
                del self.cleaned_data['source_share_code']
                raise forms.ValidationError(_('Invalid share code.'))
        return self.cleaned_data['source_share_code']


class UnsubscribeForm(forms.Form):
    """
    Form used to unsubscribe and subscriber.
    """
    email = forms.CharField(label=_('Email address'))

    def clean_email(self):
        if not Subscriber.objects.filter(email=self.cleaned_data['email']).exists():
            del self.cleaned_data['email']
            raise forms.ValidationError(_('Invalid email address.'))
        return self.cleaned_data['email']
