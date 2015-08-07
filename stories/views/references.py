from django.contrib import messages
from django.utils.translation import ugettext as _

from k2.utils.django.views.generic.combined import create_object_detail

from utils import check_url

def create_reference_detail(request, **kwargs):
    if request.method == 'GET' and 'url' in request.GET:
        try:
            url, title = check_url(request.GET['url'])
            kwargs.setdefault('extra_context', {}).update({'parsed_url': url, 'parsed_title': title,})
        except IOError, e:
            messages.error(request, _(e), fail_silently=True)
    return create_object_detail(request, **kwargs)
