# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djinn_pages', '0002_menuitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ['-order']},
        ),
        migrations.AddField(
            model_name='menuitem',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
