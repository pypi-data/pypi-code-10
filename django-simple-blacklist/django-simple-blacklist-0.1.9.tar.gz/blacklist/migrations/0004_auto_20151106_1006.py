# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0003_auto_20151016_0541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Country', 'verbose_name_plural': 'Countries', 'ordering': ('code',)},
        ),
        migrations.AddField(
            model_name='blockrules',
            name='subnet',
            field=models.CharField(null=True, verbose_name='Subnet', max_length=20, blank=True),
        ),
    ]
