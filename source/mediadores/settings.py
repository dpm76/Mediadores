# -*- coding: utf-8 -*-

# Django settings for mediadores project.
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('David', 'davidpm@dpm-ingenieria.es'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'registro_mediadores',                      # Or path to database file if using sqlite3.
        'USER': 'dbuser.mediacion',                      # Not used with sqlite3.
        'PASSWORD': 'd@m0c1es',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ES'

#Idiomas disponibles para la interfaz de usuario.
#Si la petición llega en otro idioma, se utilizará el idioma definido en
# LANGUAGE_CODE
UI_LANGUAGES = ['es']

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SITE_URL_ROOT = "http://mediacioncameral.org"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

STATIC_DOC_ROOT = PROJECT_ROOT + '/static-files/'
STATIC_DOC_URL = '/static-files/'
APP_LOGO_URL = STATIC_DOC_URL + 'img/logo.png'
NO_IMAGE_URL = STATIC_DOC_URL + 'img/anonymous.png'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_DOC_URL + "admin/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '72cv#3$6lal*g4&x@z1a4ku(bu%*i*wf&=yesmp7b)rgmttj50'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth', #django 1.3.1
    #'django.contrib.auth.context_processors.auth', #django 1.4.1
    'django.core.context_processors.csrf',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'mediadores.context_processors.mediators_processor',  
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mediadores.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + "/templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'django.contrib.admin',
    'mediadores.main',
    'mediadores.emailusernames',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    #'dbbackup',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'main.UserProfile'

RECAPTCHA_PUB_KEY = '6LexsdwSAAAAANeSbEIsnDBvo45Yi-Oigo4GFDEO'
RECAPTCHA_PRI_KEY = '6LexsdwSAAAAADhDK3afYt0VIDIAz0WEuAySwCWR'

AUTHENTICATION_BACKENDS = ('mediadores.emailusernames.backends.EmailAuthBackend',)

#email configuration
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.mediacioncameral.org'
EMAIL_HOST_USER = 'registro.mediacioncameral.org'
EMAIL_HOST_PASSWORD = 'd@m0c1es'
EMAIL_PORT = 25

#backup
DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_FILESYSTEM_DIRECTORY = PROJECT_ROOT + '/backup'

#Carga de configuración para desarrollo
if os.environ.get('DEVELOPMENT', None):
    from settings_dev import *

