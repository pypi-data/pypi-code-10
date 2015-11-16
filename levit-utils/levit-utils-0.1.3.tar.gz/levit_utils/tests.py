import re

from django_webtest import WebTest
from django.conf import settings


class MiddlewareTest(WebTest):

  def testHome(self):
    if 'levit_utils.middleware.LocaleMiddleware' in settings.MIDDLEWARE_CLASSES:
      index = self.app.get('/')
      self.assertEqual(index.status_code, 200)
      match = re.search(r' lang="en"', '{}'.format(index.content))
      self.assertIsNotNone(match)
      match = re.search(' lang="fr"', '{}'.format(index.content))
      self.assertIsNone(match)

      for lang in ['nl', 'es-es', 'nl-be']:
        self.app.reset()
        index = self.app.get('/', extra_environ={'HTTP_ACCEPT_LANGUAGE': lang}).maybe_follow()
        self.assertEqual(index.status_code, 200)
        match = re.search(' lang="fr"', '{}'.format(index.content))
        self.assertIsNone(match)
        match = re.search(' lang="en"', '{}'.format(index.content))
        self.assertIsNotNone(match)

      for lang in ['fr', 'fr-fr', 'fr-be']:
        self.app.reset()
        index = self.app.get('/', extra_environ={'HTTP_ACCEPT_LANGUAGE': lang}).maybe_follow()
        self.assertEqual(index.status_code, 200)
        match = re.search(' lang="en"', '{}'.format(index.content))
        self.assertIsNone(match)
        match = re.search(' lang="fr"', '{}'.format(index.content))
        self.assertIsNotNone(match)
