import unittest

from quickbooks.objects.bill import Bill, BillLine, AccountBasedExpenseLineDetail, ItemBasedExpenseLineDetail


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_unicode(self):
        acct_detail = AccountBasedExpenseLineDetail()
        acct_detail.BillableStatus = "test"

        self.assertEqual(str(acct_detail), "test")


class BillTests(unittest.TestCase):
    def test_unicode(self):
        bill = Bill()
        bill.Balance = 1000

        self.assertEqual(str(bill), "1000")


class BillLineTests(unittest.TestCase):
    def test_unicode(self):
        bill_line = BillLine()
        bill_line.Amount = 1000

        self.assertEqual(str(bill_line), "1000")


class ItemBasedExpenseLineDetailTest(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEqual(detail.BillableStatus, "")
        self.assertEqual(detail.UnitPrice, 0)
        self.assertEqual(detail.TaxInclusiveAmt, 0)
        self.assertEqual(detail.Qty, 0)
        self.assertEqual(detail.ItemRef, None)
        self.assertEqual(detail.ClassRef, None)
        self.assertEqual(detail.PriceLevelRef, None)
        self.assertEqual(detail.TaxCodeRef, None)
        self.assertEqual(detail.MarkupInfo, None)
        self.assertEqual(detail.CustomerRef, None)
