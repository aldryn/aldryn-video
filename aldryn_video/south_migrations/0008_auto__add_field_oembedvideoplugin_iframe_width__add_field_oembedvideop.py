# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from ..utils import rename_tables_old_to_new, rename_tables_new_to_old

class Migration(SchemaMigration):

    def forwards(self, orm):
        rename_tables_old_to_new(db)
        # Adding field 'OEmbedVideoPlugin.iframe_width'
        db.add_column(u'aldryn_video_oembedvideoplugin', 'iframe_width',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True),
                      keep_default=False)

        # Adding field 'OEmbedVideoPlugin.iframe_height'
        db.add_column(u'aldryn_video_oembedvideoplugin', 'iframe_height',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        rename_tables_new_to_old(db)
        # Deleting field 'OEmbedVideoPlugin.iframe_width'
        db.delete_column(u'cmsplugin_oembedvideoplugin', 'iframe_width')

        # Deleting field 'OEmbedVideoPlugin.iframe_height'
        db.delete_column(u'cmsplugin_oembedvideoplugin', 'iframe_height')


    models = {
        u'aldryn_video.oembedvideoplugin': {
            'Meta': {'object_name': 'OEmbedVideoPlugin', 'db_table': "u'cmsplugin_oembedvideoplugin'", '_ormbases': ['cms.CMSPlugin']},
            'auto_play': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'custom_params': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iframe_height': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'iframe_width': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'loop_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oembed_data': ('jsonfield.fields.JSONField', [], {'default': "u'null'", 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        # XXX intellectronica 2015-11-02 The CMSPlugin fields level, lft,
        # rght and tree_id have been commented-out in order to allow this
        # migration to run in later versions of the CMS where they do not exist.
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
