# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Transaction.withdraw_amount'
        db.alter_column(u'yamoney_transaction', 'withdraw_amount', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):

        # Changing field 'Transaction.withdraw_amount'
        db.alter_column(u'yamoney_transaction', 'withdraw_amount', self.gf('django.db.models.fields.FloatField')(default=None))

    models = {
        u'yamoney.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'codepro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'643'", 'max_length': '100'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'notification_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'operation_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'withdraw_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['yamoney']