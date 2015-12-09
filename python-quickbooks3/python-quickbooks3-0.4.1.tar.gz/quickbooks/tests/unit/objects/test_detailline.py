import unittest

from quickbooks.objects.detailline import SalesItemLineDetail, DiscountOverride, DetailLine, SubtotalLineDetail, \
    DiscountLineDetail, SubtotalLine, DescriptionLineDetail, DescriptionLine, SaleItemLine, DiscountLine


class DetailLineTests(unittest.TestCase):
    def test_unicode(self):
        detail = DetailLine()
        detail.LineNum = 1
        detail.Description = "Product Description"
        detail.Amount = 100

        self.assertEqual(str(detail), "[1] Product Description 100")


class SalesItemLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        sales_detail = SalesItemLineDetail()
        sales_detail.UnitPrice = 10

        self.assertEqual(str(sales_detail), "10")


class DiscountOverrideTests(unittest.TestCase):
    def test_init(self):
        discount_override = DiscountOverride()

        self.assertEqual(discount_override.DiscountPercent, 0)
        self.assertEqual(discount_override.DiscountRef, None)
        self.assertEqual(discount_override.DiscountAccountRef, None)
        self.assertFalse(discount_override.PercentBased)


class DiscountLineDetailTesets(unittest.TestCase):
    def test_init(self):
        discount_detail = DiscountLineDetail()

        self.assertEqual(discount_detail.Discount, None)
        self.assertEqual(discount_detail.ClassRef, None)
        self.assertEqual(discount_detail.TaxCodeRef, None)

class SubtotalLineDetailTest(unittest.TestCase):
    def test_init(self):
        detail = SubtotalLineDetail()

        self.assertEqual(detail.ItemRef, None)


class SubtotalLineTest(unittest.TestCase):
    def test_init(self):
        subtotal_line = SubtotalLine()

        self.assertEqual(subtotal_line.DetailType, "SubtotalLineDetail")
        self.assertEqual(subtotal_line.SubtotalLineDetail, None)


class DescriptionLineDetailTest(unittest.TestCase):
    def test_init(self):
        description_detail = DescriptionLineDetail()

        self.assertEqual(description_detail.ServiceDate, "")
        self.assertEqual(description_detail.TaxCodeRef, None)


class DescriptionLineTest(unittest.TestCase):
    def test_init(self):
        line = DescriptionLine()

        self.assertEqual(line.DetailType, "DescriptionOnly")
        self.assertEqual(line.DescriptionLineDetail, None)


class SaleItemLineTest(unittest.TestCase):
    def test_init(self):
        line = SaleItemLine()

        self.assertEqual(line.DetailType, "SalesItemLineDetail")
        self.assertEqual(line.SalesItemLineDetail, None)


class DiscountLineTest(unittest.TestCase):
    def test_init(self):
        line = DiscountLine()

        self.assertEqual(line.DetailType, "DiscountLineDetail")
        self.assertEqual(line.DiscountLineDetail, None)
