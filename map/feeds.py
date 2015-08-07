from django.contrib.gis.feeds import Feed as GeoFeed
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed

from k2.map.models import Location

class UserLocationsFeed(Feed):
    feed_type = GeoFeed
    title = Site.objects.get_current()
    link = "/mapa/"
    description = _("Users Map")

    def items(self):
        return Location.users.all()

    def item_link(self, obj):
        return obj.content_object.get_profile().url

    def item_geometry(self, obj):
        return obj.point.x, obj.point.y

