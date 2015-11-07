# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('seg_0', models.CharField(verbose_name='Segment 1', max_length=3)),
                ('seg_1', models.CharField(verbose_name='Segment 2', max_length=3)),
                ('seg_2', models.CharField(verbose_name='Segment 3', max_length=3)),
                ('seg_3', models.CharField(verbose_name='Segment 4', max_length=3)),
            ],
            options={
                'verbose_name': 'IP',
                'verbose_name_plural': 'IPs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationLocal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Local location',
                'verbose_name_plural': 'Local locations',
            },
            bases=(models.Model,),
        ),
    ]
