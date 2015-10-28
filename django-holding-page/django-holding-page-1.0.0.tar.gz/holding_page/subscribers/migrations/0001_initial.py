# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(unique=True, max_length=254, db_index=True)),
                ('share_code', models.CharField(max_length=10, null=True, db_index=True)),
                ('source_share_code', models.CharField(max_length=10, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('export_csv', 'Can export CSV data'),),
            },
        ),
    ]
