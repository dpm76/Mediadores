# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class MediatorInstitutionTabularInline(admin.TabularInline):
    model = models.Mediator.institution.through    

class MediatorExpertiseAreaTabularInline(admin.TabularInline):
    model = models.Mediator.expertiseArea.through
    
class MediatorDegreeTabularInline(admin.TabularInline):
    model = models.Mediator.degree.through

class MediatorTabularInline(admin.TabularInline):
    model=models.Mediator
    ordering=['surname', 'name']

class InstitutionAdminTabularInline(admin.TabularInline):
    model=models.InstitutionAdmin
    ordering = ['surname', 'name']

class DegreeTabularInline(admin.TabularInline):
    model = models.Degree
    ordering=['name']

class RequestTabularInline(admin.TabularInline):
    model=models.Request

class ExpertiseAreaTabularInline(admin.TabularInline):
    model=models.ExpertiseArea

class InstitutionStackedInline(admin.StackedInline):
    model = models.Institution
    
class InsuranceEntityStackedInline(admin.StackedInline):
    model = models.InsuranceEntity

class InstitutionModelAdmin(admin.ModelAdmin):
    inlines=[MediatorInstitutionTabularInline, InstitutionAdminTabularInline]
    search_fields=['name', 'province', 'city', 'postalcode']
    ordering=['name']
 
class ResquestModelAdmin(admin.ModelAdmin):    
    search_fields=['mediator','institution','requester_nif']
    ordering=['timestamp']
    list_filter=['timestamp']

class ExpertiseAreaModelAdmin(admin.ModelAdmin):
    ordering=['name']

class DegreeModelAdmin(admin.ModelAdmin):
    inlines=[MediatorDegreeTabularInline]
    ordering=['name']

class MediatorModelAdmin(admin.ModelAdmin):
    pass

class InsuranceEntityModelAdmin(admin.ModelAdmin):
    inlines=[MediatorTabularInline]
    ordering=['name']

admin.site.register(models.Institution, InstitutionModelAdmin)
admin.site.register(models.ExpertiseArea, ExpertiseAreaModelAdmin)
admin.site.register(models.Degree, DegreeModelAdmin)
admin.site.register(models.Request, ResquestModelAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Mediator, MediatorModelAdmin)
admin.site.register(models.InsuranceEntity, InsuranceEntityModelAdmin)
admin.site.register(models.InstitutionAdmin)