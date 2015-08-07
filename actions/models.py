from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from k2.stories.models import Story
from k2.actions import managers
from k2.actions import settings

ACTION_CHOICES = (
    (settings.ACTION_VOTE_NEGATIVE, _('gave negative vote')),
    (settings.ACTION_VOTE_POSITIVE, _('gave positive vote')), 
    (settings.ACTION_COMMENT, _('commented')),
    (settings.ACTION_STORY, _('added new story')),
    (settings.ACTION_STORY_PUBLISHED, _('story was published')),
    (settings.ACTION_REFERENCE, _('added new reference to story')),
)

class Action(models.Model):
    user            = models.ForeignKey(User, verbose_name=_('user'))
    story           = models.ForeignKey(Story, verbose_name=_('story'))
    date_added      = models.DateTimeField(_('date added'), auto_now_add=True, editable=False)
    type            = models.IntegerField(_('type'), choices=ACTION_CHOICES)

    objects = managers.ActionManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.get_type_display() + ': ' + str(self.user) + ' on ' + str(self.story)
