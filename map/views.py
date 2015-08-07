from xml.dom import minidom

from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import simplejson
from django.views.generic.create_update import update_object

from k2.map.forms import UserLocationForm
from k2.map.models import Location
from k2.map import settings

@login_required
def update_location(request, **kwargs):
    user_id = request.user.id
    Location.users.get_or_create(object_id=user_id)
    return update_object(request, object_id=user_id, **kwargs)

def geodata(request, lat, lng):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        url = "http://ws.geonames.org/countrySubdivision?lat=%s&lng=%s" % (lat, lng)
        dom = minidom.parse(urllib.urlopen(url))
        country = dom.getElementsByTagName('countryCode')
        if len(country) >=1:
            country = country[0].childNodes[0].data
        region = dom.getElementsByTagName('adminName1')
        if len(region) >=1:
            region = region[0].childNodes[0].data

        return HttpResponse(simplejson.dumps({'success': True, 'country': country, 'region': region}))
    else:
        raise Http404()

@login_required
def location(request):
    """
    Location selection of the user profile
    """
    profile = request.user.get_profile()
    geoip = hasattr(settings, "GEOIP_PATH")
    if geoip and request.method == "GET" and request.GET.get('ip') == "1":
        from django.contrib.gis.utils import GeoIP
        g = GeoIP()
        c = g.city(request.META.get("REMOTE_ADDR"))
        if c and c.get("latitude") and c.get("longitude"):
            profile.latitude = "%.6f" % c.get("latitude")
            profile.longitude = "%.6f" % c.get("longitude")
            profile.location = unicode(c.get("city"), "latin1")

    if request.method == "POST":
        form = UserLocationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile information has been updated successfully."), fail_silently=True)

            #signal_responses = signals.post_signal.send(sender=location, request=request, form=form)
            #last_response = signals.last_response(signal_responses)
            #if last_response:
            #    return last_response

    else:
        form = UserLocationForm(instance=profile)

    #signals.context_signal.send(sender=location, request=request, context=data)
    return render_to_response("map/location_form_update.html", \
        { 'GOOGLE_MAPS_API_KEY': settings.MAP_GOOGLE_MAPS_API_KEY, \
        'form': form, 'geoip': geoip }, context_instance=RequestContext(request))

