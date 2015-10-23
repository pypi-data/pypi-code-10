# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookFriend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friend_facebook_id', models.BigIntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookUserLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('category', models.CharField(max_length=250)),
                ('facebook_id', models.BigIntegerField()),
                ('created_time', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facebook_id', models.BigIntegerField(unique=True)),
                ('access_token', models.TextField(null=True, blank=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('first_name', models.TextField(null=True, blank=True)),
                ('last_name', models.TextField(null=True, blank=True)),
                ('middle_name', models.TextField(null=True, blank=True)),
                ('username', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('locale', models.CharField(max_length=5, null=True, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('birthday', models.DateField(help_text=b'needs user_birthday', null=True, blank=True)),
                ('location_name', models.TextField(help_text=b'needs user_location', null=True, blank=True)),
                ('location_id', models.TextField(help_text=b'needs user_location', null=True, blank=True)),
                ('relationship_status', models.TextField(help_text=b'needs user_relationship', null=True, blank=True)),
                ('website', models.TextField(help_text=b'needs user_website', null=True, blank=True)),
                ('about_me', models.TextField(help_text=b'needs user_about_me', null=True, blank=True)),
                ('raw_data', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='facebookuserlike',
            unique_together=set([('user', 'facebook_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='facebookfriend',
            unique_together=set([('user', 'friend_facebook_id')]),
        ),
    ]
