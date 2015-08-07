from django.conf.urls.defaults import *

urlpatterns = patterns('k2.utils.contrib.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
