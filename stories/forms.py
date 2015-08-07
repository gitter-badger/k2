from itertools import groupby
from operator import attrgetter

from django import forms
from django.utils.translation import ugettext_lazy as _

from tagging.forms import TagField

from k2.utils.django.forms import widgets
from k2.utils.django.forms.models import ModelGroupedChoiceField
from k2.utils.django.forms.html5 import widgets as html5_widgets

from k2.stories.models import Story, Reference, UserPref, Category
from k2.stories.widgets import AutoCompleteTagInput

def get_grouped_choices(queryset, group_field_name):
    choices = []
    for group, opts in groupby(queryset,
                               attrgetter(group_field_name)):
        choices.append((group, [(opt.pk, opt.name) for opt in opts]))
    return choices

class StoryAdminForm(forms.ModelForm):
    class Meta:
        model = Story
        widgets = {
            'tags': AutoCompleteTagInput,
        }

class PartialStoryForm(forms.ModelForm):
    #category = forms.ChoiceField(choices=get_grouped_choices(queryset=Category.objects.exclude(parent=None).order_by('parent', 'id'), group_field_name='parent'))

    class Meta:
        model = Story
        fields = ('url', 'title', 'summary', 'category', 'tags')
        widgets = {
            'url': html5_widgets.URLInput,
            'tags': AutoCompleteTagInput,
        }

class SubmitStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        include = ('url',)
        widgets = {
            'url': html5_widgets.URLInput(attrs={'placeholder': _('Enter URL address')}),
        }

class SubmitReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        include = ('url',)
        widgets = {
            'url': html5_widgets.URLInput(attrs={'placeholder': _('Enter URL address')}),
        }

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        widgets = {
            'url': html5_widgets.URLInput,
        }

class PartialUserPrefForm(forms.ModelForm):
    class Meta:
        model = UserPref
        exclude = ('user', 'upcoming_sort', 'popular_sort')
        widgets = {
            'comment_threshold': html5_widgets.NumberInput,
        }
