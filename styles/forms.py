from django import forms
from django.forms import widgets
from django.contrib.auth.models import User

from k2.utils.django.forms.html5 import fields as html5_fields
from k2.utils.django.forms.html5 import widgets as html5_widgets

from k2.styles import widgets as style_widgets
from k2.styles.models import UserStyle
from k2.styles import get_style_list

def get_style_choices():
    return [(s,s) for s in get_style_list()]

def get_night_style_choices():
    return [('', '---------'), ] + get_style_choices()

class UserStyleForm(forms.ModelForm):
    style = forms.ChoiceField(choices=get_style_choices())
    night_style = forms.ChoiceField(required=False, choices=get_night_style_choices())

    class Meta:
        model = UserStyle

    def clean_night_style(self):
        data = self.cleaned_data['night_style']
        if data == '':
            data = None
        return data

class PartialUserStyleForm(UserStyleForm):
    class Meta:
        model = UserStyle
        exclude = ('user',)
        widgets = {
            'style': widgets.Textarea(attrs={'cols': 80, 'rows': 20}),
            'night_style_from': html5_widgets.NumberInput(attrs={'min': 0, 'max': 23, 'size': 5}),
            'night_style_to': html5_widgets.NumberInput(attrs={'min': 0, 'max': 23, 'size': 5}),
        }
