# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_datastore', '0003_auto_20150602_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookuserprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
