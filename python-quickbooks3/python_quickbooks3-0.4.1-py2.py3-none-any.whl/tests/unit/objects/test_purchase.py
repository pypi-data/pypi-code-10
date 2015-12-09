import unittest

from quickbooks.objects.purchase import Purchase, PurchaseLine, AccountBasedExpenseLineDetail, \
    ItemBasedExpenseLineDetail


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        detail = AccountBasedExpenseLineDetail()
        detail.BillableStatus = "Test"

        self.assertEqual(str(detail), "Test")


class PurchaseLineTests(unittest.TestCase):
    def test_unicode(self):
        purchase_line = PurchaseLine()
        purchase_line.Amount = 100

        self.assertEqual(str(purchase_line), "100")


class PurchaseTests(unittest.TestCase):
    def test_unicode(self):
        purchase = Purchase()
        purchase.TotalAmt = 1000

        self.assertEqual(str(purchase), "1000")


class ItemBasedExpenseLineDetailTest(unittest.TestCase):
    def test_init(self):
        item_detail = ItemBasedExpenseLineDetail()

        self.assertEqual(item_detail.UnitPrice, 0)
        self.assertEqual(item_detail.Qty, 0)
        self.assertEqual(item_detail.BillableStatus, "")
        self.assertEqual(item_detail.TaxInclusiveAmt, 0)
        self.assertEqual(item_detail.ItemRef, None)
        self.assertEqual(item_detail.ClassRef, None)
        self.assertEqual(item_detail.PriceLevelRef, None)
        self.assertEqual(item_detail.TaxCodeRef, None)
        self.assertEqual(item_detail.CustomerRef, None)
        self.assertEqual(item_detail.MarkupInfo, None)