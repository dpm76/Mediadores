# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from mediadores import settings
from mediadores.emailusernames.forms import EmailAuthenticationForm
from mediadores.text_plain import TextPlainView

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mediadores.views.home', name='home'),
    # url(r'^mediadores/', include('mediadores.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^robots\.txt$', TextPlainView.as_view(template_name='robots.txt')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','main.views.home' ),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': EmailAuthenticationForm}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^list/(?P<institutionId>\w+)/$', 'main.views.mediators_list'),
    url(r'^request/(?P<institutionId>\w+)/(?P<mediatorNif>\w+)/$', 'main.views.do_request'),
    url(r'^contact/(?P<institutionId>\w+)/$', 'main.views.contact'),
    url(r'^contact/$', 'main.views.selectAndContact'),
    url(r'^info/(?P<institutionId>\w+)/$', 'main.views.info'),
    url(r'^edit/(?P<mediatorId>\w+)/$', 'main.views.editMediator'),
    url(r'^delete/(?P<mediatorId>\w+)/$', 'main.views.deleteMediator'),
    url(r'^add/$', 'main.views.addMediator'),
    url(r'^insurance-entities/$', 'main.views.insuranceEntities'),
    url(r'^areas/$', 'main.views.areas'),
    url(r'^degrees/$', 'main.views.degrees'),
    url(r'^legal/$', 'main.views.legal'),
    url(r'^reset-password/$', 'main.views.resetPassword'),
    url(r'^userconfig/$', 'main.views.userconfig'),
    url(r'^ajax/add-expertise-area/$','main.views.addExpertiseArea'),
    url(r'^ajax/add-degree/$','main.views.addDegree'),
    url(r'^ajax/get-nif-list/$','main.views.getNifList'),
    url(r'^ajax/get-mediator/$','main.views.getMediator'),
    url(r'^(?P<institutionId>\w+)/$', 'main.views.home_general_institution'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static-files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
