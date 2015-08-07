from django import forms

from models import Vote

class ObjectVoteForm(forms.ModelForm):
    class Meta:
        model = Vote
