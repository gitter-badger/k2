from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.gis.sitemaps.views import kml

from k2.map import settings
from k2.map.forms import UserLocationForm
from k2.map.models import Location
from k2.map.views import update_location, geodata
from k2.map.feeds import UserLocationsFeed

user_location_list_info = {
    'queryset': Location.users.all(),
    'template_object_name': 'location',
    'template_name': 'map/user_list_gm3.html',
    'extra_context': {'GOOGLE_MAPS_API_KEY': settings.MAP_GOOGLE_MAPS_API_KEY}
}

user_location_update_info = {
    'form_class': UserLocationForm,
    'template_name': 'map/user_update.html',
    'extra_context': {'GOOGLE_MAPS_API_KEY': settings.MAP_GOOGLE_MAPS_API_KEY}
}

user_location_kml_info = {
    'label': 'map',
    'model': 'Location',
    'field_name': 'point',
}

urlpatterns = patterns('map.views',
    url(r'^mapa/$', object_list, user_location_list_info, name='map'), 
    url(r'^ustawienia/mapa/$', update_location, user_location_update_info, name='settings'), 
    url(r'^getcountry_info/(?P<lat>[0-9\.\-]+)/(?P<lng>[0-9\.\-]+)/$', \
        geodata, name='geocountry_info'),
    url(r'^users\.kml$', kml, user_location_kml_info),
    (r'^rss/geo/$', UserLocationsFeed()),
)
