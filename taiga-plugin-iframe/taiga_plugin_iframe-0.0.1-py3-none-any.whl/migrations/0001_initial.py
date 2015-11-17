# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20150504_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='IframePlugin',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('url', models.URLField(verbose_name='Iframe URL')),
                ('icon', models.TextField(verbose_name='Base64-encoded icon', max_length=8092)),
                ('html', models.TextField(verbose_name='Additional HTML before iframe', max_length=8092)),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order', default=0)),
                ('project', models.ForeignKey(to='projects.Project', related_name='iframes')),
            ],
            options={
                'ordering': ['-order', 'title'],
            },
            bases=(models.Model,),
        ),
    ]
