# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Properties'
        db.create_table(u'wheelcms_properties_properties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main', self.gf('django.db.models.fields.related.ForeignKey')(related_name='properties', to=orm['wheelcms_axle.Configuration'])),
        ))
        db.send_create_signal(u'wheelcms_properties', ['Properties'])

        # Adding model 'PropertyForm'
        db.create_table(u'wheelcms_properties_propertyform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conf', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forms', to=orm['wheelcms_properties.Properties'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('form', self.gf('django.db.models.fields.TextField')(default='[]')),
            ('types', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'wheelcms_properties', ['PropertyForm'])


    def backwards(self, orm):
        # Deleting model 'Properties'
        db.delete_table(u'wheelcms_properties_properties')

        # Deleting model 'PropertyForm'
        db.delete_table(u'wheelcms_properties_propertyform')


    models = {
        u'wheelcms_axle.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'analytics': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'head': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailto': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'sendermail': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'})
        },
        u'wheelcms_properties.properties': {
            'Meta': {'object_name': 'Properties'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': u"orm['wheelcms_axle.Configuration']"})
        },
        u'wheelcms_properties.propertyform': {
            'Meta': {'object_name': 'PropertyForm'},
            'conf': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forms'", 'to': u"orm['wheelcms_properties.Properties']"}),
            'form': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'types': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['wheelcms_properties']