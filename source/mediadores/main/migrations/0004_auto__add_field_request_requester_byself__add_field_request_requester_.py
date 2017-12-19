# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Request.requester_byself'
        db.add_column('main_request', 'requester_byself', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Request.requester_representee'
        db.add_column('main_request', 'requester_representee', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True), keep_default=False)

        # Adding field 'Request.requester_fax'
        db.add_column('main_request', 'requester_fax', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True), keep_default=False)

        # Adding field 'Request.requester_address_street'
        db.add_column('main_request', 'requester_address_street', self.gf('django.db.models.fields.CharField')(default='NA', max_length=128), keep_default=False)

        # Adding field 'Request.requester_address_floor'
        db.add_column('main_request', 'requester_address_floor', self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True), keep_default=False)

        # Adding field 'Request.requester_address_postcode'
        db.add_column('main_request', 'requester_address_postcode', self.gf('django.db.models.fields.CharField')(default='NA', max_length=8), keep_default=False)

        # Adding field 'Request.requester_address_city'
        db.add_column('main_request', 'requester_address_city', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Request.requester_address_province'
        db.add_column('main_request', 'requester_address_province', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True), keep_default=False)

        # Adding field 'Request.requester_party'
        db.add_column('main_request', 'requester_party', self.gf('django.db.models.fields.CharField')(default='NA', max_length=256), keep_default=False)

        # Adding field 'Request.opponent_party'
        db.add_column('main_request', 'opponent_party', self.gf('django.db.models.fields.CharField')(default='NA', max_length=256), keep_default=False)

        # Adding field 'Request.mediation_mode'
        db.add_column('main_request', 'mediation_mode', self.gf('django.db.models.fields.CharField')(default='0', max_length=1), keep_default=False)

        # Changing field 'Request.requester_email'
        db.alter_column('main_request', 'requester_email', self.gf('django.db.models.fields.EmailField')(max_length=64, null=True))

        # Changing field 'Request.requester_mobile'
        db.alter_column('main_request', 'requester_mobile', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Request.requester_phone'
        db.alter_column('main_request', 'requester_phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Request.requester_byself'
        db.delete_column('main_request', 'requester_byself')

        # Deleting field 'Request.requester_representee'
        db.delete_column('main_request', 'requester_representee')

        # Deleting field 'Request.requester_fax'
        db.delete_column('main_request', 'requester_fax')

        # Deleting field 'Request.requester_address_street'
        db.delete_column('main_request', 'requester_address_street')

        # Deleting field 'Request.requester_address_floor'
        db.delete_column('main_request', 'requester_address_floor')

        # Deleting field 'Request.requester_address_postcode'
        db.delete_column('main_request', 'requester_address_postcode')

        # Deleting field 'Request.requester_address_city'
        db.delete_column('main_request', 'requester_address_city')

        # Deleting field 'Request.requester_address_province'
        db.delete_column('main_request', 'requester_address_province')

        # Deleting field 'Request.requester_party'
        db.delete_column('main_request', 'requester_party')

        # Deleting field 'Request.opponent_party'
        db.delete_column('main_request', 'opponent_party')

        # Deleting field 'Request.mediation_mode'
        db.delete_column('main_request', 'mediation_mode')

        # Changing field 'Request.requester_email'
        db.alter_column('main_request', 'requester_email', self.gf('django.db.models.fields.EmailField')(default='none@none', max_length=64))

        # Changing field 'Request.requester_mobile'
        db.alter_column('main_request', 'requester_mobile', self.gf('django.db.models.fields.CharField')(default='NA', max_length=32))

        # Changing field 'Request.requester_phone'
        db.alter_column('main_request', 'requester_phone', self.gf('django.db.models.fields.CharField')(default='NA', max_length=32))


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
            'insuranceContract': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'insuranceEntity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.InsuranceEntity']", 'null': 'True', 'blank': 'True'}),
            'insuranceExpiration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nif': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.UserProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'main.request': {
            'Meta': {'object_name': 'Request'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Institution']"}),
            'mediation_mode': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'mediator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Mediator']"}),
            'opponent_party': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'purpose': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'requester_address_city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'requester_address_floor': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'requester_address_postcode': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'requester_address_province': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'requester_address_street': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'requester_byself': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requester_email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'requester_fax': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'requester_mobile': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'requester_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requester_nif': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'requester_party': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'requester_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'requester_representee': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
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
