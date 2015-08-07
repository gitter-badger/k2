from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from k2.actions.views import action_list
from k2.actions.models import Action

action_list_info = {
    'queryset': Action.objects.all()[:15],
}

urlpatterns = patterns('actions.views',
    url(r'^obserwatorium/$', login_required(action_list), action_list_info, 'action_list'), 
)
