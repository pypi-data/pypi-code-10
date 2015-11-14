# -*- coding: utf-8 -*-

from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from . import load_class
from .settings import WRITEBACK_BASE_FORM
from .models import Message


class MessageCreateFormBase(ModelForm):
    class Meta:
        model = Message
        exclude = ['date_created']

    def clean(self):
        cleaned_data = super(MessageCreateFormBase, self).clean()
        name = cleaned_data.get("name")
        family_name = cleaned_data.get("family_name")
        company = cleaned_data.get("company")
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        info = cleaned_data.get("info")

        if not (name or family_name or company or phone or email or info):
            raise ValidationError(_("Please, fill out at least one field."))

        return super(MessageCreateFormBase, self).clean()


class MessageCreateForm(load_class(WRITEBACK_BASE_FORM)):
    pass
