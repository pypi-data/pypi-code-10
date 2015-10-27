# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='git_server_connstr',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='git_staging_connstr',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
