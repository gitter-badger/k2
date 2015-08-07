from django import forms

from k2.map import settings
from k2.map.models import Location
from k2.map.widgets import PointWidget

class UserLocationForm(forms.ModelForm):
    point = forms.CharField(widget=PointWidget())

    class Meta:
        model = Location
        exclude = ("content_type","object_id")
    class Media:
        js = ("http://maps.google.com/maps?file=api&v=2.x&key=%s" % settings.MAP_GOOGLE_MAPS_API_KEY, "http://www.openlayers.org/dev/OpenLayers.js",)

