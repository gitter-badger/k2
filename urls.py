from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
#from django.contrib.gis import admin

from djangobb_forum import settings as forum_settings

from k2.utils.registration.forms import RegistrationFormUniqueNoFreeEmailTOS

# HACK for add default_params with RegistrationFormUtfUsername and backend to registration urlpattern
# Must be changed after django-authopenid #50 (signup-page-does-not-work-whih-django-registration)
# will be fixed
from django_authopenid.urls import urlpatterns as authopenid_urlpatterns
for i, rurl in enumerate(authopenid_urlpatterns):
    if rurl.name == 'registration_register':
        authopenid_urlpatterns[i].default_args.update({'form_class': RegistrationFormUniqueNoFreeEmailTOS})
#                                                  'backend': 'registration.backends.default.DefaultBackend'})
#    elif rurl.name == 'registration_activate':
#                authopenid_urlpatterns[i].default_args = {'backend': 'registration.backends.default.DefaultBackend'}

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin
    (r'^admin/', include(admin.site.urls)),
    # profiles
    (r'^', include('k2.profiles.urls', namespace='profiles')),
    # styles
    (r'^', include('k2.styles.urls', namespace='styles')),
    # map
    #(r'^', include('k2.map.urls', namespace='map')),
    # comments
    (r'^komentarze/', include('k2.utils.threadedcomments.urls', namespace='comments')),
    # forum
    (r'^kontakt/', include('k2.contact.urls', namespace='contact')),
    # forum
    (r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),
    # announcements
    (r"^announcements/", include("announcements.urls")),
    # actions
    (r'^', include('k2.actions.urls', namespace='actions')),
    # stories (must be last)
    (r'^', include('k2.stories.urls', namespace='stories')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

# PM Extension
if forum_settings.PM_SUPPORT:
    urlpatterns += patterns('',
        (r'^forum/pm/', include('messages.urls')),
   )

# feeds
#from k2.map.feeds import UserLocationsFeed

#feeds = {
#    'geo': UserLocationsFeed,
#}

#urlpatterns += patterns('',
#    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
#        {'feed_dict': feeds}),
#)
