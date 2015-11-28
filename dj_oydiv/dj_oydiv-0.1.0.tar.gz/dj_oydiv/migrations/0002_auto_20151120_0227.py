# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_oydiv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vidyoadmin',
            name='user_location_tag',
            field=models.CharField(default=b'Node4', help_text='Default location tag for new users (router affinity) formultiple router configuration.', max_length=128, verbose_name='Location Tag'),
        ),
        migrations.AlterField(
            model_name='vidyoadmin',
            name='user_proxy',
            field=models.CharField(default=b'ExternalProxy VR2', help_text='Default Proxy name for TCP tunneling of conferences', max_length=128, verbose_name='Default Proxy'),
        ),
    ]
