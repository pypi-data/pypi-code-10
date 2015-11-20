# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geokey_import', '0002_dataimport_imported'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataimport',
            name='geom_field',
            field=models.CharField(default='geom', max_length=100),
            preserve_default=False,
        ),
    ]
