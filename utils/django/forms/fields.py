from django.forms import fields

from widgets import RemovableFileWidget

class RemovableFileField(fields.MultiValueField):
    widget = RemovableFileWidget
    field = fields.FileField
    def __init__(self, *args, **kwargs):
        field_list = [self.field(*args, **kwargs), fields.BooleanField(required=False)]
        super(RemovableFileField, self).__init__(field_list, required=False)
    def compress(self, data_list):
        return data_list

class RemovableImageField(RemovableFileField):
    field = fields.ImageField
