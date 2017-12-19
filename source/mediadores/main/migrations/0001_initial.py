# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Institution'
        db.create_table('main_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('institutionType', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('main', ['Institution'])

        # Adding model 'UserProfile'
        db.create_table('main_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal('main', ['UserProfile'])

        # Adding model 'ExpertiseArea'
        db.create_table('main_expertisearea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ExpertiseArea'], null=True)),
        ))
        db.send_create_signal('main', ['ExpertiseArea'])

        # Adding model 'Degree'
        db.create_table('main_degree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('expertiseArea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ExpertiseArea'])),
        ))
        db.send_create_signal('main', ['Degree'])

        # Adding model 'Mediator'
        db.create_table('main_mediator', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.UserProfile'], unique=True, primary_key=True)),
            ('nif', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('postalCode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=4096, blank=True)),
        ))
        db.send_create_signal('main', ['Mediator'])

        # Adding M2M table for field institution on 'Mediator'
        db.create_table('main_mediator_institution', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediator', models.ForeignKey(orm['main.mediator'], null=False)),
            ('institution', models.ForeignKey(orm['main.institution'], null=False))
        ))
        db.create_unique('main_mediator_institution', ['mediator_id', 'institution_id'])

        # Adding M2M table for field degree on 'Mediator'
        db.create_table('main_mediator_degree', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediator', models.ForeignKey(orm['main.mediator'], null=False)),
            ('degree', models.ForeignKey(orm['main.degree'], null=False))
        ))
        db.create_unique('main_mediator_degree', ['mediator_id', 'degree_id'])

        # Adding model 'InstitutionAdmin'
        db.create_table('main_institutionadmin', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.UserProfile'], unique=True, primary_key=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Institution'])),
        ))
        db.send_create_signal('main', ['InstitutionAdmin'])

        # Adding model 'Request'
        db.create_table('main_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mediator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Mediator'])),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Institution'])),
            ('requester_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('requester_surname', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('requester_nif', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('requester_phone', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('requester_mobile', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('requester_email', self.gf('django.db.models.fields.EmailField')(max_length=64)),
            ('purpose', self.gf('django.db.models.fields.TextField')(max_length=2048)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['Request'])

    def backwards(self, orm):
        # Deleting model 'Institution'
        db.delete_table('main_institution')

        # Deleting model 'UserProfile'
        db.delete_table('main_userprofile')

        # Deleting model 'ExpertiseArea'
        db.delete_table('main_expertisearea')

        # Deleting model 'Degree'
        db.delete_table('main_degree')

        # Deleting model 'Mediator'
        db.delete_table('main_mediator')

        # Removing M2M table for field institution on 'Mediator'
        db.delete_table('main_mediator_institution')

        # Removing M2M table for field degree on 'Mediator'
        db.delete_table('main_mediator_degree')

        # Deleting model 'InstitutionAdmin'
        db.delete_table('main_institutionadmin')

        # Deleting model 'Request'
        db.delete_table('main_request')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.degree': {
            'Meta': {'object_name': 'Degree'},
            'expertiseArea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ExpertiseArea']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'main.expertisearea': {
            'Meta': {'object_name': 'ExpertiseArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ExpertiseArea']", 'null': 'True'})
        },
        'main.institution': {
            'Meta': {'object_name': 'Institution'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutionType': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        'main.institutionadmin': {
            'Meta': {'object_name': 'InstitutionAdmin', '_ormbases': ['main.UserProfile']},
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Institution']"}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.mediator': {
            'Meta': {'object_name': 'Mediator', '_ormbases': ['main.UserProfile']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'degree': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Degree']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'institution': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Institution']", 'symmetrical': 'False'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.UserProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        'main.request': {
            'Meta': {'object_name': 'Request'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Institution']"}),
            'mediator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Mediator']"}),
            'purpose': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'requester_email': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'requester_mobile': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'requester_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requester_nif': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'requester_phone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'requester_surname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['main']