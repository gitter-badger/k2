from django.contrib.gis import admin

from k2.map.admin import GoogleAdmin
from k2.map.models import Location

# Getting an instance so we can generate the map widget; also
# getting the geometry field for the model.
admin_instance = GoogleAdmin(Location, admin.site)
point_field = Location._meta.get_field('point')

# Generating the widget.
PointWidget = admin_instance.get_map_widget(point_field)

