# -*- coding: utf-8 -*-
from django.contrib import admin
from yamoney.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'withdraw_amount', 'amount', 'currency', 'datetime',)

    def has_add_permission(self, request):
        return False


admin.site.register(Transaction, TransactionAdmin)