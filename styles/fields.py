from django.db import models
from django import forms

from south.modelsinspector import add_introspection_rules

from k2.styles import validators

class WidthFormField(forms.CharField):
    default_validators = [validators.validate_width]
    
class WidthField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': WidthFormField}
        defaults.update(kwargs)
        return super(WidthField, self).formfield(**defaults)

add_introspection_rules([], ["^k2\.styles\.fields\.WidthField"])
