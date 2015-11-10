from unittest import TestCase
from unicore.languages.constants import LANGUAGES


class LanguagesTestCase(TestCase):
    def test_total_languages(self):
        self.assertEqual(len(LANGUAGES), 437)
