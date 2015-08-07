from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from k2.map import managers

class Location(models.Model):
    content_type    = models.ForeignKey(ContentType, \
        related_name="content_type_set_for_%(class)s")
    object_id       = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    point           = models.PointField(srid=4326)
    name            = models.CharField(_('name'),max_length=50, blank=True)
    last_edit_date  = models.DateTimeField(editable=False, auto_now=True)

    # overriding the default manager with a GeoManager instance.
    objects = models.GeoManager()
    users = managers.UserManager()
    class Meta:
        ordering = ('-last_edit_date',)
        get_latest_by = 'last_edit_date'

    def __unicode__(self):
        return "%s: %s" % (str(self.content_object), self.name)

