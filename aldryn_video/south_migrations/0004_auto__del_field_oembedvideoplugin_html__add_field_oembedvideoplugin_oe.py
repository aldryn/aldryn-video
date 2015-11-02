# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from ..utils import rename_tables_old_to_new, rename_tables_new_to_old

class Migration(SchemaMigration):

    def forwards(self, orm):
        rename_tables_old_to_new(db)
        # Deleting field 'OEmbedVideoPlugin.html'
        db.delete_column(u'aldryn_video_oembedvideoplugin', 'html')

        # Adding field 'OEmbedVideoPlugin.oembed_data'
        db.add_column(u'aldryn_video_oembedvideoplugin', 'oembed_data',
                      self.gf('jsonfield.fields.JSONField')(default=u'null', null=True),
                      keep_default=False)


    def backwards(self, orm):
        rename_tables_new_to_old(db)
        # Adding field 'OEmbedVideoPlugin.html'
        db.add_column(u'cmsplugin_oembedvideoplugin', 'html',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'OEmbedVideoPlugin.oembed_data'
        db.delete_column(u'cmsplugin_oembedvideoplugin', 'oembed_data')


    models = {
        u'aldryn_video.oembedvideoplugin': {
            'Meta': {'object_name': 'OEmbedVideoPlugin', 'db_table': "u'cmsplugin_oembedvideoplugin'", '_ormbases': ['cms.CMSPlugin']},
            'auto_play': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loop_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oembed_data': ('jsonfield.fields.JSONField', [], {'default': "u'null'", 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'use_lightbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            # 'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            # 'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            # 'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            # 'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_video']
