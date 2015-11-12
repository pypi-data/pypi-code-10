# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(help_text='Screen name of the Twitter account to sync.', max_length=125, verbose_name='Twitter Account')),
                ('is_active', models.BooleanField(default=True, help_text='Mark this account enabled for syncing?', verbose_name='Active?')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date Added')),
                ('updated', models.DateTimeField(default=datetime.datetime.now, verbose_name='Last Updated')),
            ],
            options={
                'ordering': ('screen_name',),
                'verbose_name': 'Twitter Account',
                'verbose_name_plural': 'Twitter Accounts',
            },
        ),
        migrations.CreateModel(
            name='TwitterStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_id', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(verbose_name='Created At')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('author', models.ForeignKey(related_name='tweets', to='twittersync.TwitterAccount')),
            ],
            options={
                'ordering': ('-created_date',),
                'get_latest_by': 'created_date',
                'verbose_name': 'Twitter Status',
                'verbose_name_plural': 'Twitter Statuses',
            },
        ),
    ]
