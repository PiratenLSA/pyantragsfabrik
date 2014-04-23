# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Type'
        db.create_table('antragsfabrik_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('last_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('antragsfabrik', ['Type'])

        # Adding model 'HistoricalApplication'
        db.create_table('antragsfabrik_historicalapplication', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('typ_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True, blank=True)),
            ('author_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('reasons', self.gf('django.db.models.fields.TextField')()),
            ('discussion', self.gf('django.db.models.fields.URLField')(null=True, max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('proofed_form', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('proofed_form_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('proofed_form_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('proofed_form_user_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('history_user', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('antragsfabrik', ['HistoricalApplication'])

        # Adding model 'Application'
        db.create_table('antragsfabrik_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('typ', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['antragsfabrik.Type'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('reasons', self.gf('django.db.models.fields.TextField')()),
            ('discussion', self.gf('django.db.models.fields.URLField')(null=True, max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('proofed_form', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('proofed_form_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('proofed_form_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('proofed_form_user', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='proofed_form_user_related', blank=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('antragsfabrik', ['Application'])

        # Adding model 'HistoricalLQFBInitiative'
        db.create_table('antragsfabrik_historicallqfbinitiative', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('antrag_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pro', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('contra', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('neutral', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('history_user', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'])),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('antragsfabrik', ['HistoricalLQFBInitiative'])

        # Adding model 'LQFBInitiative'
        db.create_table('antragsfabrik_lqfbinitiative', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('antrag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['antragsfabrik.Application'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pro', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('contra', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('neutral', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('antragsfabrik', ['LQFBInitiative'])

        # Adding model 'UserProfile'
        db.create_table('antragsfabrik_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User'])),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('antragsfabrik', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Type'
        db.delete_table('antragsfabrik_type')

        # Deleting model 'HistoricalApplication'
        db.delete_table('antragsfabrik_historicalapplication')

        # Deleting model 'Application'
        db.delete_table('antragsfabrik_application')

        # Deleting model 'HistoricalLQFBInitiative'
        db.delete_table('antragsfabrik_historicallqfbinitiative')

        # Deleting model 'LQFBInitiative'
        db.delete_table('antragsfabrik_lqfbinitiative')

        # Deleting model 'UserProfile'
        db.delete_table('antragsfabrik_userprofile')


    models = {
        'antragsfabrik.application': {
            'Meta': {'object_name': 'Application'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'proofed_form': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'proofed_form_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'proofed_form_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'proofed_form_user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'proofed_form_user_related'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'reasons': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'typ': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['antragsfabrik.Type']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'antragsfabrik.historicalapplication': {
            'Meta': {'object_name': 'HistoricalApplication', 'ordering': "('-history_date', '-history_id')"},
            'author_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'discussion': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'proofed_form': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'proofed_form_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'proofed_form_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'proofed_form_user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'reasons': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'typ_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'antragsfabrik.historicallqfbinitiative': {
            'Meta': {'object_name': 'HistoricalLQFBInitiative', 'ordering': "('-history_date', '-history_id')"},
            'antrag_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'contra': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'neutral': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pro': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'antragsfabrik.lqfbinitiative': {
            'Meta': {'object_name': 'LQFBInitiative'},
            'antrag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['antragsfabrik.Application']"}),
            'contra': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neutral': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pro': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'antragsfabrik.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'antragsfabrik.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['antragsfabrik']