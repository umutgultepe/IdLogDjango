# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.creationDate'
        db.add_column('logs_category', 'creationDate',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 7, 28, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category.creationDate'
        db.delete_column('logs_category', 'creationDate')


    models = {
        'logs.category': {
            'Meta': {'object_name': 'Category'},
            'categoryName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'logs.logentry': {
            'Meta': {'object_name': 'LogEntry'},
            'activeFlag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logs.Category']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'entryDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'logs.relation': {
            'Meta': {'object_name': 'Relation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preceeder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Preceeding Entry'", 'to': "orm['logs.LogEntry']"}),
            'succeeder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Succeeding Entry'", 'to': "orm['logs.LogEntry']"})
        }
    }

    complete_apps = ['logs']