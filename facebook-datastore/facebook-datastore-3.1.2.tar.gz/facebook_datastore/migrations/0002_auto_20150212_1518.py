# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_datastore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookuserprofile',
            name='age_range_max',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebookuserprofile',
            name='age_range_min',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebookuserprofile',
            name='uses_android',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebookuserprofile',
            name='uses_ios',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
