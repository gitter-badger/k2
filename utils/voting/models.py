from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from managers import VoteManager

SCORES_CHOICES = (
    (  4, u'+4'),
    (  3, u'+3'),
    (  2, u'+2'),
    (  1, u'+1'),
    (  0, u' 0'),
    ( -1, u'-1'),
    ( -2, u'-2'),
    ( -3, u'-3'),
    ( -4, u'-4'),
)

REASON_NO                   = 0
REASON_CHOICE_UNSUITABLE    = 1
REASON_CHOICE_DUPLICATE     = 2
REASON_CHOICE_MISLEADING    = 3
REASON_CHOICE_SPAM          = 4
REASON_CHOICE_INAPPROPRIATE = 5

REASON_CHOICES = (
    (REASON_NO, '---------'),
    (REASON_CHOICE_SPAM, _('spam')),
    (REASON_CHOICE_DUPLICATE, _('duplicate')),
    (REASON_CHOICE_MISLEADING, _('misleading')),
    (REASON_CHOICE_UNSUITABLE, _('unsuitable')),
    (REASON_CHOICE_INAPPROPRIATE, _('inappropriate')),
)

class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    user         = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id    = models.PositiveIntegerField()
    object       = generic.GenericForeignKey('content_type', 'object_id')
    vote         = models.SmallIntegerField(choices=SCORES_CHOICES)
    reason = models.PositiveSmallIntegerField(choices=REASON_CHOICES, \
        default=REASON_NO)
    date_modified = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        # One vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)


    def __unicode__(self):
        return u'%s: %s on %s' % (self.user, self.vote, self.object)


    def is_upvote(self):
        return self.vote > 0


    def is_downvote(self):
        return self.vote < 0