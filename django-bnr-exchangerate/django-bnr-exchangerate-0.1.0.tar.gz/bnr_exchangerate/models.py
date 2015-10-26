import datetime
from decimal import Decimal

from django.db import models


class ExchangeRate(models.Model):
    date = models.DateField()
    currency = models.CharField(max_length=3, db_index=True)
    value = models.DecimalField(max_digits=15, decimal_places=4)
    multiplier = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def get_rate(self, currency, date):
        day = datetime.datetime.strptime(date, '%Y-%m-%d')
        if day.weekday() == 5:
            day = day - datetime.timedelta(days=1)
        elif day.weekday() == 6:
            day = day - datetime.timedelta(days=2)
        try:
            rate = ExchangeRate.objects.get(currency=currency.upper(), date=day.strftime('%Y-%m-%d'))
        except ExchangeRate.DoesNotExist:
            return False
        return Decimal(rate.value)

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')

    class Meta:
        unique_together = ('date', 'currency')