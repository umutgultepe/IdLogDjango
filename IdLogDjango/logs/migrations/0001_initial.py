# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('logs_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoryName', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('logs', ['Category'])

        # Adding model 'LogEntry'
        db.create_table('logs_logentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logs.Category'])),
            ('entryDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastModified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('activeFlag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('logs', ['LogEntry'])

        # Adding model 'Relation'
        db.create_table('logs_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preceeder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Preceeding Entry', to=orm['logs.LogEntry'])),
            ('succeeder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Succeeding Entry', to=orm['logs.LogEntry'])),
        ))
        db.send_create_signal('logs', ['Relation'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('logs_category')

        # Deleting model 'LogEntry'
        db.delete_table('logs_logentry')

        # Deleting model 'Relation'
        db.delete_table('logs_relation')


    models = {
        'logs.category': {
            'Meta': {'object_name': 'Category'},
            'categoryName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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