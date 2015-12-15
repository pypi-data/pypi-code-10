# -*- coding: utf-8 -*-
from django.dispatch import Signal


transaction_success = Signal(providing_args=["related_obj"])