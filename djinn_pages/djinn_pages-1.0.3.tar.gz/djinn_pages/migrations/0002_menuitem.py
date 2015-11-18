# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djinn_pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('url', models.CharField(default=b'#', max_length=256, null=True, blank=True)),
                ('parent', models.ForeignKey(default=None, blank=True, to='djinn_pages.MenuItem', null=True)),
            ],
        ),
    ]
