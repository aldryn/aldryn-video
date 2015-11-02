# -*- coding: utf-8 -*-
import datetime
import re
from south.db import db
from south.v2 import DataMigration
from django.db import models

from aldryn_video.utils import get_embed_code

from ..utils import rename_tables_old_to_new, rename_tables_new_to_old

IFRAME_SRC_REGEX = 'src="([^"]+)"'


class Migration(DataMigration):

    def get_oembed_params(self, plugin):
        extra = {}
        if plugin.width:
            extra['maxwidth'] = plugin.width
        if plugin.height:
            extra['maxheight'] = plugin.height
        if plugin.auto_play:
            extra['autoplay'] = 1
        if plugin.loop_video:
            extra['loop'] = 1
        return extra

    def forwards(self, orm):
        "Write your forwards methods here."
        rename_tables_old_to_new(db)
        for plugin in orm.oembedvideoplugin.objects.all():
            # Depending on the amount of plugins, this could take a while.
            data = get_embed_code(url=plugin.url, **self.get_oembed_params(plugin))
            player_url = re.search(IFRAME_SRC_REGEX, data.get('html', ''))
            if player_url:
                data['player_url'] = player_url.groups()[0]
            plugin.oembed_data = data
            plugin.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        rename_tables_new_to_old(db)

    models = {
        u'aldryn_video.oembedvideoplugin': {
            'Meta': {'object_name': 'OEmbedVideoPlugin', '_ormbases': ['cms.CMSPlugin']},
            'auto_play': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loop_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oembed_data': ('jsonfield.fields.JSONField', [], {'default': "u'null'", 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'use_lightbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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

    from distutils.version import LooseVersion
    import cms
    if LooseVersion(cms.__version__) >= LooseVersion('3.1'):
        models['cms.cmsplugin'] = {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }

    complete_apps = ['aldryn_video']
    symmetrical = True
