# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from yamoney.models import Transaction


class TransactionTestCase(TestCase):

    def test_transaction_create(self):
        """Transaction must be created"""
        test_data = {
            'notification_type': Transaction.NOTIFICATION_TYPE_CHOICES[0][0],
            'operation_id': '123',
            'amount': 100,
            'withdraw_amount': 100,
            'datetime': timezone.now(),
            'sender': '9999999999',
            'codepro': False
        }
        test_obj = Transaction.objects.create(**test_data)
        transaction = Transaction(**test_data)
        transaction.label = Transaction.generate_label(test_obj)
        transaction.save()
        self.assertEqual(transaction.get_related_obj(), test_obj)