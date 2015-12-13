# -*- coding: utf-8 -*-
from hashlib import sha1
from django import forms
from yamoney import settings as yamoney_settings
from yamoney.models import Transaction
from yamoney.fields import DateTimeISO6801Field


class YandexPaymentForm(forms.Form):
    ACTION_URL = 'https://money.yandex.ru/quickpay/confirm.xml'
    QUICKPAY_CHOICES = (
        ('shop', 'shop'),
        ('donate', 'donate'),
        ('small', 'small'),
    )
    PAYMENTTYPE_CHOICES = (
        ('PC', u'оплата со счета Яндекс.Денег'),
        ('AC', u'оплата с банковской карты')
    )
    FIELD_NAME_MAPPING = {
        'shortDest': 'short-dest',
        'quickpayForm': 'quickpay-form',
    }
    receiver = forms.CharField(widget=forms.HiddenInput)
    formcomment = forms.CharField(max_length=50, widget=forms.HiddenInput)
    shortDest = forms.CharField(max_length=50, widget=forms.HiddenInput)
    quickpayForm = forms.ChoiceField(choices=QUICKPAY_CHOICES, initial='shop', widget=forms.HiddenInput)
    targets = forms.CharField(max_length=150, widget=forms.HiddenInput)
    sum = forms.FloatField(widget=forms.HiddenInput)
    paymentType = forms.ChoiceField(label=u'Варианты оплаты', choices=PAYMENTTYPE_CHOICES,
                                    initial='AC',
                                    widget=forms.RadioSelect)
    label = forms.CharField(required=False, widget=forms.HiddenInput)
    # comment = forms.CharField(required=False, max_length=200, widget=forms.HiddenInput)

    def add_prefix(self, field_name):
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(YandexPaymentForm, self).add_prefix(field_name)


class YandexNotificationForm(forms.ModelForm):
    datetime = DateTimeISO6801Field()
    sha1_hash = forms.CharField()

    class Meta:
        model = Transaction

    def make_hash(self):
        cd = self.data
        return sha1('&'.join(map(str, (
            cd.get('notification_type', ''),
            cd.get('operation_id', ''),
            cd.get('amount', ''),
            cd.get('currency', ''),
            cd.get('datetime', ''),
            cd.get('sender', ''),
            cd.get('codepro', ''),
            yamoney_settings.NOTIFICATION_SECRET,
            cd.get('label', ''),
        )))).hexdigest()
    
    def clean(self):
        cd = super(YandexNotificationForm, self).clean()
        sha1_hash = cd.get('sha1_hash')
        if sha1_hash != self.make_hash():
            raise forms.ValidationError(u'Хэш не совпадает')
        return cd


def paymentform_factory(targets, sum, label):
    initial = {
        'receiver': yamoney_settings.ACCOUNT,
        'formcomment': yamoney_settings.FORM_COMMENT or targets,
        'shortDest': targets,
        'targets': targets,
        'sum': sum,
        'label': label,
    }
    return YandexPaymentForm(initial=initial)