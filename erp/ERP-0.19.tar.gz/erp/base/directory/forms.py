__author__ = 'cltanuki'
from django import forms
from .models import Person, Address, EMail, Phone
from django.forms.models import inlineformset_factory


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['user']

AddressFormSet = inlineformset_factory(Person, Address, extra=1)
PhoneFormSet = inlineformset_factory(Person, Phone, extra=1)
EMailFormSet = inlineformset_factory(Person, EMail, extra=1)