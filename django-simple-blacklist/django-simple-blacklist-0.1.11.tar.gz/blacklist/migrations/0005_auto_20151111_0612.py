# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import blacklist.utils


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0004_auto_20151106_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockrules',
            name='reason',
            field=models.CharField(default='Not Known', max_length=500, verbose_name='Reason'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blockrules',
            name='subnet',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Subnet', validators=[blacklist.utils.subnet_validator]),
            preserve_default=True,
        ),
    ]
