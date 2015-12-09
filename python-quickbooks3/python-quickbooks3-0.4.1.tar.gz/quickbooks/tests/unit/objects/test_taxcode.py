import unittest

from quickbooks.objects.taxcode import TaxCode, TaxRateDetail, TaxRateList


class TaxCodeTests(unittest.TestCase):
    def test_unicode(self):
        taxcode = TaxCode()
        taxcode.Name = "test"

        self.assertEqual(str(taxcode), "test")

class TaxRateDetailTests(unittest.TestCase):
    def test_init(self):
        tax_rate = TaxRateDetail()

        self.assertEqual(tax_rate.TaxOrder, 0)
        self.assertEqual(tax_rate.TaxTypeApplicable, "")


class TaxRateListTests(unittest.TestCase):
    def test_init(self):
        tax_rate_list = TaxRateList()

        self.assertEqual(tax_rate_list.TaxRateDetail, [])
