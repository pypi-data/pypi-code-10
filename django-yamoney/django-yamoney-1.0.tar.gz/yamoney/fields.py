# -*- coding: utf-8 -*-
import dateutil.parser
from django import forms


class DateTimeISO6801Field(forms.DateTimeField):

    def strptime(self, value, format):
        return dateutil.parser.parse(value)