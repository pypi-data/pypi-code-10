# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
            options={
                'verbose_name': 'menu',
                'verbose_name_plural': 'menus',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=50, verbose_name='caption')),
                ('url', models.CharField(max_length=200, verbose_name='URL', blank=True)),
                ('named_url', models.CharField(max_length=200, verbose_name='named URL', blank=True)),
                ('level', models.IntegerField(default=0, verbose_name='level', editable=False)),
                ('rank', models.IntegerField(default=0, verbose_name='rank', editable=False)),
                ('menu', models.ForeignKey(related_name='contained_items', blank=True, editable=False, to='treemenus.Menu', null=True, verbose_name='menu')),
                ('parent', models.ForeignKey(verbose_name='parent', blank=True, to='treemenus.MenuItem', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='root_item',
            field=models.ForeignKey(related_name='is_root_item_of', blank=True, editable=False, to='treemenus.MenuItem', null=True, verbose_name='root item'),
        ),
    ]
