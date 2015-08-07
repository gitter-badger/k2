from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from invitation.models import InvitationKey

inviter = models.OneToOneField(User, related_name='invitations', unique=True)

last_update = models.DateTimeField(_('last update time'), auto_now_add=True)

registrant = models.OneToOneField(User, related_name='invitation_used', null=True, \
    blank=True, unique=True)
