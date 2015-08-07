from django.contrib.gis import admin
from django.contrib.gis.maps.google import GoogleMap

from k2.map import settings
from k2.map.models import Location

GMAP = GoogleMap(key=settings.MAP_GOOGLE_MAPS_API_KEY)

class GoogleAdmin(admin.OSMGeoAdmin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    map_height = 325

class LocationAdmin(admin.OSMGeoAdmin):
    list_select_related = True
    list_filter = ('content_type','point' )
    list_display = ('__unicode__', 'point', 'content_type', 'object_id')
    # Default GeoDjango OpenLayers map options
    # Uncomment and modify as desired
    # To learn more about this jargon visit:
    # www.openlayers.org
    
    #default_lon = 0
    #default_lat = 0
    #default_zoom = 4
    #display_wkt = False
    #display_srid = False
    #extra_js = []
    #num_zoom = 18
    #max_zoom = False
    #min_zoom = False
    #units = False
    #max_resolution = False
    max_resolution = "156543.0339"
    #max_extent = False
    #modifiable = True
    #mouse_position = True
    #scale_text = True
    #layerswitcher = True
    scrollable = False
    #admin_media_prefix = settings.ADMIN_MEDIA_PREFIX
    map_width = 700
    map_height = 325
    #map_srid = 4326
    #map_template = 'gis/admin/openlayers.html'
    openlayers_url = 'http://openlayers.org/api/2.9.1/OpenLayers.js'
    #wms_url = 'http://labs.metacarta.com/wms/vmap0'
    #wms_layer = 'basic'
    #wms_name = 'OpenLayers WMS'
    #debug = False
    #widget = OpenLayersWidget

admin.site.register(Location, GoogleAdmin)
#admin.site.register(Location, LocationAdmin)
#admin.site.register(UserLocation, UserLocationAdmin)

