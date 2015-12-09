import unittest

from quickbooks.objects.deposit import Deposit, DepositLine, AttachableRef, CashBackInfo, DepositLineDetail


class DepositTests(unittest.TestCase):
    def test_unicode(self):
        deposit = Deposit()
        deposit.TotalAmt = 100

        self.assertEqual(str(deposit), "100")


class DepositLineTests(unittest.TestCase):
    def test_unicode(self):
        deposit = DepositLine()
        deposit.Amount = 100

        self.assertEqual(str(deposit), "100")


class AttachableRefTests(unittest.TestCase):
    def test_init(self):
        attachable_ref = AttachableRef()

        self.assertEqual(attachable_ref.LineInfo, "")
        self.assertFalse(attachable_ref.IncludeOnSend)
        self.assertFalse(attachable_ref.Inactive)
        self.assertFalse(attachable_ref.NoRefOnly)
        self.assertEqual(attachable_ref.EntityRef, None)


class CashBackInfoTests(unittest.TestCase):
    def test_init(self):
        cash_back_info = CashBackInfo()

        self.assertEqual(cash_back_info.Amount, 0)
        self.assertEqual(cash_back_info.Memo, "")
        self.assertEqual(cash_back_info.AccountRef, None)


class DepositLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DepositLineDetail()

        self.assertEqual(detail.Entity, None)
        self.assertEqual(detail.ClassRef, None)
        self.assertEqual(detail.AccountRef, None)
        self.assertEqual(detail.PaymentMethodRef, None)
        self.assertEqual(detail.CheckNum, "")
        self.assertEqual(detail.TxnType, "")
