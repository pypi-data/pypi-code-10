# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_remove_page_section_ptr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='order',
        ),
    ]
