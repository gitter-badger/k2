"Porfiles views module"
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from k2.profiles.models import UserProfile

def change_password_done(request, **kwargs):
    messages.add_message(request, messages.INFO, _('Password change successful'))
    return HttpResponseRedirect(kwargs['post_change_redirect'])
