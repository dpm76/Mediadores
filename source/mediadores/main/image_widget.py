from PIL import Image
from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
import os
import time

def thumbnail(image_path):
    absolute_url = os.path.join(settings.MEDIA_URL, image_path)
    return u'<img class="imgWidget" src="%s?token=%d" alt="%s" />' % (absolute_url, time.time(), image_path)

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    template_with_initial = (u'<p class="file-upload"> %(clear_template)s<br />%(input_text)s: %(input)s </p>')
    template_with_clear = (u'<span class="clearable-file-input">%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label></span>')
    
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name and file_name != "None":
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<table><tr><td><a target="_blank" href="%s">%s</a></td><td>' % \
                    (file_path, thumbnail(file_name),))
            except IOError: # not image
                output.append('<table><tr><td>No es una imagen</td><td>')
            
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if file_name and file_name != "None":
            output.append('</td></tr></table>')
        return mark_safe(u''.join(output))