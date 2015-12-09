import unittest

from quickbooks.objects.purchaseorder import PurchaseOrderLine, PurchaseOrder, ItemBasedExpenseLineDetail


class PurchaseOrderLineTests(unittest.TestCase):
    def test_unicode(self):
        purchase_line = PurchaseOrderLine()
        purchase_line.Amount = 100

        self.assertEqual(str(purchase_line), '100')


class PurchaseOrderTests(unittest.TestCase):
    def test_unicode(self):
        purchase_order = PurchaseOrder()
        purchase_order.TotalAmt = 1000

        self.assertEqual(str(purchase_order), '1000')


class ItemBasedExpenseLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEqual(detail.UnitPrice, 0)
        self.assertEqual(detail.Qty, 0)
        self.assertEqual(detail.BillableStatus, "")
        self.assertEqual(detail.TaxInclusiveAmt, 0)
        self.assertEqual(detail.PriceLevelRef, None)
        self.assertEqual(detail.CustomerRef, None)
        self.assertEqual(detail.ClassRef, None)
        self.assertEqual(detail.TaxCodeRef, None)
        self.assertEqual(detail.MarkupInfo, None)
