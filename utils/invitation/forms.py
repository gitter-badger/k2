from django import forms
from django.utils.translation import ugettext_lazy as _

from k2.utils.django.forms.html5 import widgets as html5_widgets

class InvitationKeyForm(forms.Form):
    email = forms.EmailField(widget=html5_widgets.EmailInput(attrs={'placeholder': _('Enter e-mail address'),}))