'''
Created on 14/01/2013

@author: David
'''
from django.utils.translation import activate
from mediadores import settings
import time

def mediators_processor(request):
    
    if request.LANGUAGE_CODE[:2] in settings.UI_LANGUAGES:        
        languageCode = request.LANGUAGE_CODE
    else:
        languageCode = settings.LANGUAGE_CODE
        activate(languageCode)
    
    return {
            'APP_LOGO_URL': settings.APP_LOGO_URL,
            'DEBUG': settings.DEBUG,
            'MEDIA_URL': settings.MEDIA_URL,
            'LANGUAGE_CODE': languageCode,
            'STATIC_DOC_URL': settings.STATIC_DOC_URL,
            'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX, 
            'NO_IMAGE_URL': settings.NO_IMAGE_URL,
            'RECAPTCHA_PUB_KEY': settings.RECAPTCHA_PUB_KEY,
            'TIMESTAMP': time.time(),          
            }
        