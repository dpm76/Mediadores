# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'InsuranceEntity'
        db.create_table('main_insuranceentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('eMail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('postalCode', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('main', ['InsuranceEntity'])

        # Adding field 'Mediator.expertiseDescription'
        db.add_column('main_mediator', 'expertiseDescription', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True), keep_default=False)

        # Adding field 'Mediator.insuranceEntity'
        db.add_column('main_mediator', 'insuranceEntity', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['main.InsuranceEntity']), keep_default=False)

        # Adding field 'Mediator.insuranceContract'
        db.add_column('main_mediator', 'insuranceContract', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True), keep_default=False)

        # Adding field 'Mediator.insuranceExpiration'
        db.add_column('main_mediator', 'insuranceExpiration', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 12, 25), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'InsuranceEntity'
        db.delete_table('main_insuranceentity')

        # Deleting field 'Mediator.expertiseDescription'
        db.delete_column('main_mediator', 'expertiseDescription')

        # Deleting field 'Mediator.insuranceEntity'
        db.delete_column('main_mediator', 'insuranceEntity_id')

        # Deleting field 'Mediator.insuranceContract'
        db.delete_column('main_mediator', 'insuranceContract')

        # Deleting field 'Mediator.insuranceExpiration'
        db.delete_column('main_mediator', 'insuranceExpiration')


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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ExpertiseArea']", 'null': 'True', 'blank': 'True'})
        },
        'main.institution': {
            'Meta': {'object_name': 'Institution'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutionType': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'main.institutionadmin': {
            'Meta': {'object_name': 'InstitutionAdmin', '_ormbases': ['main.UserProfile']},
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Institution']"}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.insuranceentity': {
            'Meta': {'object_name': 'InsuranceEntity'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'eMail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'main.mediator': {
            'Meta': {'object_name': 'Mediator', '_ormbases': ['main.UserProfile']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'degree': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Degree']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'blank': 'True'}),
            'expertiseDescription': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Institution']", 'symmetrical': 'False'}),
            'insuranceContract': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'insuranceEntity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.InsuranceEntity']"}),
            'insuranceExpiration': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.UserProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
