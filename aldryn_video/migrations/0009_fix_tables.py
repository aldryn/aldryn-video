# -*- coding: utf-8 -*-
import re
import json

from south.db import db
from south.v2 import DataMigration
from django.db import models, connection

from aldryn_video.utils import get_embed_code


class Migration(DataMigration):
    """
    This migration is supposed to fix all issues regarding table names once and for all
    """

    def forwards(self, orm):
        # Introspection functions
        def get_table_records(table):
            return db.execute('SELECT * from %s' % table)

        def table_is_migrated(table):
            description = connection.introspection.get_table_description(connection.cursor(), table)
            haystack = [c[0] for c in description]
            needles = ['auto_play', 'loop_video', 'oembed_data', 'custom_params', 'iframe_width', 'iframe_height']
            return all(needle in haystack for needle in needles)

        def migrate_data(from_table, to_table):
            """
            from_table is not migrated, to_table is
            """
            data_list = get_table_records(from_table)
            sql = 'INSERT INTO %s (cmsplugin_ptr_id, url, width, height, auto_play, loop_video, oembed_data, ' \
                  'custom_params, iframe_width, iframe_height) VALUES ' % to_table
            for record in data_list:
                iframe_width = re.search('width="(\d+)"', record[4])
                iframe_width = iframe_width.groups()[0] if iframe_width else 'null'

                iframe_height = re.search('height="(\d+)"', record[4])
                iframe_height = iframe_height.groups()[0] if iframe_width else 'null'

                # get embed code
                if record[2] and record[3]:
                    embed_code = get_embed_code(url=record[1], maxwidth=record[2], maxheight=record[3])
                elif record[2]:
                    embed_code = get_embed_code(url=record[1], maxwidth=record[2])
                elif record[3]:
                    embed_code = get_embed_code(url=record[1], maxheight=record[3])
                else:
                    embed_code = get_embed_code(url=record[1])

                new_record_data = {
                    'cmsplugin_ptr_id': record[0],
                    'url': record[1],
                    'width': record[2] or 'null',
                    'height': record[3] or 'null',
                    'auto_play': 'false',
                    'loop_video': 'false',
                    'embed_code': json.dumps(embed_code),
                    'custom_params': '',
                    'iframe_width': iframe_width,
                    'iframe_height': iframe_height,
                }

                new_record_sql = \
                    "(%(cmsplugin_ptr_id)i, '%(url)s', %(width)s, %(height)s, %(auto_play)s, %(loop_video)s, " \
                    "'%(embed_code)s', '%(custom_params)s', %(iframe_width)s, %(iframe_height)s)," % new_record_data

                sql += new_record_sql

            sql = sql[:-1] + ';'
            return db.execute(sql)

        # Setup
        old_table = 'cmsplugin_oembedvideoplugin'
        new_table = 'aldryn_video_oembedvideoplugin'

        # Prior Introspection
        all_table_names = connection.introspection.table_names()

        old_table_exists = old_table in all_table_names
        new_table_exists = new_table in all_table_names

        old_table_has_data = bool(get_table_records(old_table)) if old_table_exists else False
        new_table_has_data = bool(get_table_records(new_table)) if new_table_exists else False

        old_table_is_migrated = table_is_migrated(old_table) if old_table_exists else False
        new_table_is_migrated = table_is_migrated(new_table) if new_table_exists else False

        # Migrating
        if not old_table_is_migrated and not new_table_is_migrated:
            raise Exception('migrations have been skipped')

        if not old_table_exists and new_table_exists:
            # how it should be
            pass

        elif old_table_exists and not new_table_exists:
            # exec_task('rename old table to new name')
            db.rename_table(old_table, new_table)

        elif old_table_exists and new_table_exists:
            if old_table_has_data and not new_table_has_data:
                if old_table_is_migrated:
                    db.delete_table(new_table)

                else:
                    migrate_data(old_table, new_table)
                    db.delete_table(old_table)

            elif not old_table_has_data and new_table_has_data:
                if new_table_is_migrated:
                    db.delete_table(old_table)

                else:
                    migrate_data(new_table, old_table)
                    db.delete_table(new_table)
                    db.rename_table(old_table, new_table)

            elif old_table_has_data and new_table_has_data:
                if new_table_is_migrated:
                    migrate_data(old_table, new_table)
                    db.delete_table(old_table)

                else:
                    migrate_data(new_table, old_table)
                    db.delete_table(new_table)
                    db.rename_table(old_table, new_table)

    def backwards(self, orm):
        pass

    models = {
        u'aldryn_video.oembedvideoplugin': {
            'Meta': {'object_name': 'OEmbedVideoPlugin', '_ormbases': ['cms.CMSPlugin']},
            'auto_play': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [],
                               {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'custom_params': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iframe_height': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'iframe_width': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'loop_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oembed_data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [],
                       {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': (
                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_video']
    symmetrical = True
