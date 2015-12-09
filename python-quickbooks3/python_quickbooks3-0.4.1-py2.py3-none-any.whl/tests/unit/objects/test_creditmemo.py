import unittest

from quickbooks.objects.creditmemo import SalesItemLineDetail, CreditMemoLine, CreditMemo, \
    DiscountLineDetail, SubtotalLineDetail, DiscountOverride, DescriptionLineDetail


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = SalesItemLineDetail()
        detail.UnitPrice = 10

        self.assertEqual(str(detail), "10")


class CreditMemoLineTests(unittest.TestCase):
    def test_unicode(self):
        memo_line = CreditMemoLine()
        memo_line.LineNum = 1
        memo_line.Description = "Product Description"
        memo_line.Amount = 100

        self.assertEqual(str(memo_line), "[1] Product Description 100")


class CreditMemoTests(unittest.TestCase):
    def test_unicode(self):
        credit_memo = CreditMemo()
        credit_memo.TotalAmt = 1000

        self.assertEqual(str(credit_memo), "1000")


class DiscountLineDetailTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEqual(discount_detail.ClassRef, None)
        self.assertEqual(discount_detail.TaxCodeRef, None)
        self.assertEqual(discount_detail.Discount, None)


class SubtotalLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = SubtotalLineDetail()

        self.assertEqual(detail.ItemRef, None)


class DiscountOverrideTests(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountOverride()

        self.assertEqual(discount_detail.PercentBased, False)
        self.assertEqual(discount_detail.DiscountPercent, 0)
        self.assertEqual(discount_detail.DiscountAccountRef, None)
        self.assertEqual(discount_detail.DiscountRef, None)


class DescriptionLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DescriptionLineDetail()

        self.assertEqual(detail.ServiceDate, "")
        self.assertEqual(detail.TaxCodeRef, None)
