"Styles models module"

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from k2.styles import settings
from k2.styles import fields as style_fields

HOUR_CHOICES = [(x,str(x)+':00') for x in range(0, 24)]

def get_styles(self):
    s, created = UserStyle.objects.get_or_create(user=self)
    return s

class Style:
    def __init__(self, title, media='screen, projection', alternate=False, filename=None):
        self.title, self.media, self.alternate, self.filename = \
            title, media, alternate, filename
        if self.filename == None:
            self.filename = self.title
        self.url = "%s%s/%s.css" % (settings.STYLES_URL, self.title, self.filename)

class UserStyle(models.Model):
    user = models.OneToOneField(User, related_name='style', verbose_name=_('user'), unique=True)
    style = models.CharField(_('style'), max_length=255, blank=True,default=settings.STYLES_DEFAULT)
    night_style = models.CharField(_('night style'), max_length=255, null=True)
    night_style_from = models.PositiveSmallIntegerField(_('night style activation hour'), choices=HOUR_CHOICES, default=22)
    night_style_to = models.PositiveSmallIntegerField(_('night style deactivation hour'), choices=HOUR_CHOICES, default=6)
    max_width = style_fields.WidthField(_('style max width'), max_length=50, help_text=_('For example: 1000px, 60%, auto or leave empty.'), blank=True)

    class Meta:
        verbose_name = _('user style')
        verbose_name_plural = _('user styles')

    def __unicode__(self):
        return self.user.username

