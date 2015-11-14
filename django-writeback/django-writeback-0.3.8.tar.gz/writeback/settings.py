# -*- coding: utf-8 -*-

from django.conf import settings


WRITEBACK_BASE_MODEL = getattr(settings, 'WRITEBACK_MESSAGE_BASE_MODEL', 'writeback.models.MessageAbstract')
WRITEBACK_BASE_FORM = getattr(settings, 'WRITEBACK_MESSAGE_BASE_FORM', 'writeback.forms.MessageCreateFormBase')

