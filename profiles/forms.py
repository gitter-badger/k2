from django import forms

from k2.utils.django.forms.html5 import widgets as html5_widgets
from k2.utils.django.forms import widgets

from k2.profiles.models import UserProfile

class PartialProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('avatar', 'user')
        widgets = {
            'website': html5_widgets.URLInput,
            'gg': html5_widgets.NumberInput,
        }

class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
