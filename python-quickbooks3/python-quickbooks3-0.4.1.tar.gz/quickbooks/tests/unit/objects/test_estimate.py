import unittest

from quickbooks.objects.estimate import Estimate


class EstimateTests(unittest.TestCase):
    def test_unicode(self):
        estimate = Estimate()
        estimate.TotalAmt = 10

        self.assertEqual(str(estimate), "10")
