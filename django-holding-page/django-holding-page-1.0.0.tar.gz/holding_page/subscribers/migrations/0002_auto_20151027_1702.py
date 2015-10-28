# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='share_code',
            field=models.CharField(db_index=True, max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='source_share_code',
            field=models.CharField(db_index=True, max_length=36, blank=True, null=True),
        ),
    ]
