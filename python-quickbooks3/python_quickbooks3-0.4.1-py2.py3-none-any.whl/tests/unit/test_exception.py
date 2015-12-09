import unittest
from mock import patch

from quickbooks.exceptions import QuickbooksException


class QuickbooksExceptionTests(unittest.TestCase):
    def test_init(self):
        exception = QuickbooksException("message", 100, "detail")

        self.assertEqual(exception.message, "message")
        self.assertEqual(exception.error_code, 100)
        self.assertEqual(exception.detail, "detail")
