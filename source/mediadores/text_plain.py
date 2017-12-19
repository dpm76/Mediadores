'''
Created on 02/03/2013

@author: david
'''
from django.views.generic.base import TemplateView

class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(context, content_type='text/plain', **kwargs)