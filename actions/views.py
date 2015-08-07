from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response
from django.template import RequestContext

def action_list(request, queryset, allow_empty=True, extra_context=None, \
        template_object_name='action', mimetype=None):
    """
    List of actions.

    Templates: ``actions/action_list.html``
    Context:
        object_list
            list of objects
    """
    if extra_context is None: extra_context = {}
    c = {
        '%s_list' % template_object_name: queryset,
        'paginator': None,
        'page_obj': None,
        'is_paginated': False,
    }
    if not allow_empty and len(queryset) == 0:
        raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    return render_to_response("actions/action_list.html", c, \
                context_instance=RequestContext(request), mimetype=mimetype)
