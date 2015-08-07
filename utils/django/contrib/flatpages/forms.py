from django import forms
from django.contrib.flatpages.models import FlatPage

class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage

    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
            'js/tiny_mce/textareas.js',)

class FlatPageEditForm(FlatPageForm):
    class Meta:
        model = FlatPage
        exclude = ('sites',)

