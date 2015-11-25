# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_auto_20151125_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='rainbows',
            name='name',
            field=models.CharField(default='', unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
