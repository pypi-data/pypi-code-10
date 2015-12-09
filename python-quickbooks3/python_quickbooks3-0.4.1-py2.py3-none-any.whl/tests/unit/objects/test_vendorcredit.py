import unittest

from quickbooks.objects.vendorcredit import VendorCredit, ItemBasedExpenseLineDetail, ItemBasedExpenseLine, \
    AccountBasedExpenseLineDetail, AccountBasedExpenseLine


class VendorCreditTests(unittest.TestCase):
    def test_unicode(self):
        vendor_credit = VendorCredit()
        vendor_credit.TotalAmt = 1000

        self.assertEqual(str(vendor_credit), "1000")


class ItemBasedExpenseLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLineDetail()

        self.assertEqual(detail.BillableStatus, "")
        self.assertEqual(detail.UnitPrice, 0)
        self.assertEqual(detail.Qty, 0)
        self.assertEqual(detail.TaxInclusiveAmt, 0)


class ItemBasedExpenseLineTests(unittest.TestCase):
    def test_init(self):
        detail = ItemBasedExpenseLine()

        self.assertEqual(detail.DetailType, "ItemBasedExpenseLineDetail")
        self.assertEqual(detail.ItemBasedExpenseLineDetail, None)


class AccountBasedExpenseLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = AccountBasedExpenseLineDetail()

        self.assertEqual(detail.BillableStatus, "")
        self.assertEqual(detail.TaxAmount, 0)
        self.assertEqual(detail.TaxInclusiveAmt, 0)


class AccountBasedExpenseLineTests(unittest.TestCase):
    def test_init(self):
        detail = AccountBasedExpenseLine()

        self.assertEqual(detail.DetailType, "AccountBasedExpenseLineDetail")
        self.assertEqual(detail.AccountBasedExpenseLineDetail, None)
