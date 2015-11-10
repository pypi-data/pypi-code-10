# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Counter', fields ['name']
        db.create_unique(u'django_generic_counter_counter', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Counter', fields ['name']
        db.delete_unique(u'django_generic_counter_counter', ['name'])


    models = {
        u'django_generic_counter.counter': {
            'Meta': {'object_name': 'Counter'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['django_generic_counter']