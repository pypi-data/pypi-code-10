# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils import formats


class Transaction(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('p2p-incoming', u'Перевод из кошелька'),
        ('card-incoming', u'Перевод с карты'),
    )
    CURRENCY_CHOICES = (
        ('643', u'руб.'),
    )

    notification_type = models.CharField(u'Тип операции', max_length=100, choices=NOTIFICATION_TYPE_CHOICES)
    operation_id = models.CharField(u'Идентификатор операции', max_length=255)
    amount = models.FloatField(u'Сумма, которая зачислена на счет получателя')
    withdraw_amount = models.FloatField(u'Сумма, которая списана со счета отправителя', blank=True, null=True)
    currency = models.CharField(u'Валюта', max_length=100, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])
    datetime = models.DateTimeField(u'Дата и время совершения перевода')
    sender = models.CharField(u'Номер счета отправителя', max_length=255, blank=True,
                              help_text=u'Только для переводов из кошелька')
    codepro = models.BooleanField(u'Служебное')
    label = models.CharField(u'Метка платежа', max_length=255, blank=True)

    class Meta:
        verbose_name = u'Перевод'
        verbose_name_plural = u'Переводы'

    def __unicode__(self):
        return u'%s на сумму %.2f %s от %s' % (
            self.get_notification_type_display(),
            self.withdraw_amount or 0,
            self.get_currency_display(),
            formats.date_format(timezone.localtime(self.datetime), 'DATETIME_FORMAT')
        )