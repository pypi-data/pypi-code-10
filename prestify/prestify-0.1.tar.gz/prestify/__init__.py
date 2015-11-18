# -*- coding: utf-8 -*-
from prestify.client import Report


try:
	from django.conf import settings
	Report.PRESTIFY_SERVICE_URL = settings.PRESTIFY_SERVICE_URL
except (ImportError, AttributeError):
	pass
