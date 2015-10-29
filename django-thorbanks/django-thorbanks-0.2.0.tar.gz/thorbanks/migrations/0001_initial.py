# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('status', models.CharField(default='P', verbose_name='Status', choices=[('P', 'Pending'), ('F', 'Failed'), ('C', 'Completed')], max_length=1)),
                ('bank_name', models.CharField(verbose_name='Bank', max_length=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('redirect_after_success', models.CharField(max_length=255, editable=False)),
                ('redirect_on_failure', models.CharField(max_length=255, editable=False)),
                ('raw_response', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Authentication',
                'ordering': ['-last_modified'],
                'abstract': False,
            },
        ),
    ]
