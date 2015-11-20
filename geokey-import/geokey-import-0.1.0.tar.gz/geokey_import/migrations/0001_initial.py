# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0013_auto_20150130_1440'),
        ('projects', '0005_auto_20150202_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('csv_file', models.FileField(upload_to=b'user-uploads/imports')),
                ('fields', django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=100), blank=True)),
                ('category', models.ForeignKey(blank=True, to='categories.Category', null=True)),
                ('project', models.ForeignKey(related_name='imports', to='projects.Project')),
            ],
        ),
    ]
