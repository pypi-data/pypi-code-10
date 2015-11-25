# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rainbows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colors', models.ManyToManyField(to='testapp.Color')),
            ],
        ),
        migrations.RemoveField(
            model_name='animals',
            name='owners',
        ),
        migrations.AddField(
            model_name='animals',
            name='owner',
            field=models.ForeignKey(default=1, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
