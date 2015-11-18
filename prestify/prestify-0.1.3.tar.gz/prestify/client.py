# -*- coding: utf-8 -*-
import base64
import json
try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode

import requests


class Report(object):
	PRESTIFY_SERVICE_URL = None

	def __init__(self, name=None):
		self.name = name
		self.format = 'pdf'
		self._parameters = dict()

	def set(self, key, value):
		self._parameters[key] = value

	def get(self, key):
		if key in self._parameters:
			return self._parameters[key]
		return None

	def fetch(self):
		if self.format not in ('pdf', 'rtf', 'xls', 'xlsx', 'html'):
			raise Exception('Invalid format')

		if self.format == 'html':
			return self.get_url()

		request = requests.get(str(self))
		return request.content

	def get_url(self):
		if self.format != 'html':
			raise Exception('URL can only be obtained for an html report')

		request = requests.get(str(self))
		return '{0}{1}'.format(self.PRESTIFY_SERVICE_URL, request.headers['Location'])

	def __str__(self):
		return '{0}/reports/{1}?{2}'.format(
			self.PRESTIFY_SERVICE_URL,
			self.name,
			urlencode(dict(format=self.format, parameters=base64.b64encode(
				json.dumps(self._parameters).encode('utf-8')
			)))
		)
