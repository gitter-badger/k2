from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _

from threadedcomments.forms import ThreadedCommentForm

class AuthThreadedCommentForm(ThreadedCommentForm):
    """Authenticated threaded comment form without title field"""
    name          = forms.CharField(label=_("Name"), max_length=50, widget=forms.HiddenInput)
    email         = forms.EmailField(label=_("Email address"), widget=forms.HiddenInput)
    url           = forms.URLField(label=_("URL"), required=False, widget=forms.HiddenInput)
    parent        = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent=None, data=None, initial=None):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(ThreadedCommentForm, self).__init__(target_object, data=data,
            initial=initial)

    def get_comment_create_data(self):
        d = super(ThreadedCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        d.pop('user_url')
        return d
