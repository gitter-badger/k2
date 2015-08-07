"""Profiles models module"""

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from k2.utils.django.db import models as extra_models

from k2.profiles import managers
from k2.profiles import settings

GENDER_CHOICE_UNKNOWN, GENDER_CHOICE_MALE, GENDER_CHOICE_FEMALE = 0, 1, 2

GENDER_CHOICES = (
    (GENDER_CHOICE_UNKNOWN, _('unknown')),
    (GENDER_CHOICE_MALE, _('male')),
    (GENDER_CHOICE_FEMALE, _('female')),
)

USERCLASS_CHOICE_BANNED, USERCLASS_CHOICE_ROOKIE, USERCLASS_CHOICE_NEW, USERCLASS_CHOICE_NORMAL, \
    USERCLASS_CHOICE_ADVANCED = 0, 1, 2, 3, 4

USERCLASS_CHOICES = (
    (USERCLASS_CHOICE_BANNED, _('Banned')),
    (USERCLASS_CHOICE_ROOKIE, _('Rookie')),
    (USERCLASS_CHOICE_NEW, _('New')),
    (USERCLASS_CHOICE_NORMAL, _('Normal')),
    (USERCLASS_CHOICE_ADVANCED, _('Advanced')),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='profile', unique=True)
    gg = models.PositiveIntegerField(_('Gadu-Gadu'), blank=True, null=True)
    jabber = extra_models.JabberField(_('jabber ID'), blank=True, null=True)
    skype = models.CharField(_('skype'), max_length=50, blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)
    about = models.TextField(_('about'), blank=True)
    location = models.CharField(_('location'), max_length=255, blank=True)
    avatar = extra_models.ImageWithThumbsField(_('avatar'), upload_to=settings.AVATAR_DIR, default=settings.AVATAR_DEFAULT_URL, sizes=settings.AVATAR_SIZES, help_text=_('Upload image file to use as your avatar'), null=True)
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, default=GENDER_CHOICE_UNKNOWN)
    email_show = models.BooleanField(_('show e-mail'), help_text=_('If selected e-mail address will be visible for other users.'), default=False)
    # karma
    rank = models.PositiveIntegerField(_('rank'), null=True, editable=False)
    karma_updated = models.DateTimeField(_('karma last update date'), auto_now_add=True)
    karma = models.IntegerField(_('karma'), default=0, null=True, editable=False)
    userclass = models.PositiveSmallIntegerField(_('user class'), choices=USERCLASS_CHOICES, default=USERCLASS_CHOICE_ROOKIE)
    # invites
    #invites_updated = models.DateTimeField(_('invites last update date'), auto_now_add=True, editable=False)
    #invites = models.PositiveSmallIntegerField(_('invites'), default=0, editable=False)
    #invite_from = models.ForeignKey(User, verbose_name=_('invited by'), related_name='invited', blank=True, null=True, editable=False)

    objects = managers.ProfileManager()

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __unicode__(self):
        return self.user.username

    @property
    def url(self):
        return reverse('profiles:profile', args=[self.user.username])

    def get_vote_weight(self):
        if self.userclass == USERCLASS_CHOICE_ROOKIE:
            return settings.VOTE_WEIGHT_ROOKIE
        if self.userclass == USERCLASS_CHOICE_NEW:
            return settings.VOTE_WEIGHT_NEW
        if self.userclass == USERCLASS_CHOICE_NORMAL:
            return settings.VOTE_WEIGHT_NORMAL
        if self.userclass == USERCLASS_CHOICE_ADVANCED:
            return settings.VOTE_WEIGHT_ADVANCED
        return 0