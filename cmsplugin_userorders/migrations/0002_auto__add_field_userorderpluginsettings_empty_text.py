# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'UserOrderPluginSettings.empty_text'
        db.add_column('cmsplugin_userorderpluginsettings', 'empty_text', self.gf('tinymce.models.HTMLField')(default="You haven't placed any orders yet."), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'UserOrderPluginSettings.empty_text'
        db.delete_column('cmsplugin_userorderpluginsettings', 'empty_text')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cmsplugin_userorders.userorderpluginsettings': {
            'Meta': {'object_name': 'UserOrderPluginSettings', 'db_table': "'cmsplugin_userorderpluginsettings'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'container_template': ('django.db.models.fields.CharField', [], {'default': "('default', 'cmsplugin_userorders/container/default.html')", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'empty_text': ('tinymce.models.HTMLField', [], {'default': '"You haven\'t placed any orders yet."'}),
            'filter_states': ('cmsplugin_userorders.fields.MultiSelectField', [], {'max_length': '32', 'blank': 'True'}),
            'item_template': ('django.db.models.fields.CharField', [], {'default': "'cmsplugin_userorders/item/default.html'", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'sort_by': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['cmsplugin_userorders']
