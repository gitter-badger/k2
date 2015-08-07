from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.xheaders import populate_xheaders
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import list_detail

def object_detail(request, current_user=True, *args, **kwargs):
    ''' update __init__ of the form class to use current user as initial if current_user'''
    if current_user:
        kwargs['slug_field'], kwargs['slug'] = 'user', request.user.id
        kwargs['form_class'] = get_current_user_form_class(kwargs['form_class'], request.user.id)
    return create_update.update_object(request, *args, **kwargs)
    
def object_detail_list(request, queryset, object_id=None, slug=None, slug_field='slug', 
            paginate_by=None, page=None, allow_empty=True, list_queryset=None, related_field='object_id',
            template_name=None, template_name_field=None, template_loader=loader,
            extra_context=None, context_processors=None, template_object_name='object',
            template_object_list_name='list', mimetype=None):
    '''
    Generic detail of an object with its related list
    
    Templates: ``<app_label>/<model_name>_detail_list.html``
    Context:
        object
            the object
        related_field
            field name in list objects for relation with detail object
        list_queryset
            queryset for list objects
    '''
    if extra_context is None: extra_context = {}
    # object detail part
    model = queryset.model
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError("Generic detail list view must be called with either an object_id or a slug/slug_field.")
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404("No %s found matching the query" % (model._meta.verbose_name))
    # object list part
    list_queryset = list_queryset._clone()
    try:
        list_queryset = list_queryset.filter(**{related_field: obj})
    except Exception:
        raise AttributeError("Generic detail list view must be used with detail and list objects within correct relation")
    if paginate_by:
        paginator = Paginator(list_queryset, paginate_by, allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        c = RequestContext(request, {
            template_object_name: obj,
            '%s_list' % template_object_list_name: page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,

            # Legacy template context stuff. New templates should use page_obj
            # to access this instead.
            'is_paginated': page_obj.has_other_pages(),
            'results_per_page': paginator.per_page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page': page_obj.number,
            'next': page_obj.next_page_number(),
            'previous': page_obj.previous_page_number(),
            'first_on_page': page_obj.start_index(),
            'last_on_page': page_obj.end_index(),
            'pages': paginator.num_pages,
            'hits': paginator.count,
            'page_range': paginator.page_range,
        }, context_processors)
    else:
        c = RequestContext(request, {
            template_object_name: obj,
            '%s_list' % template_object_list_name: list_queryset,
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
        }, context_processors)
        if not allow_empty and len(list_queryset) == 0:
            raise Http404
    # template part
    if not template_name:
        template_name = "%s/%s_detail_list.html" % (model._meta.app_label, model._meta.object_name.lower())
    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    response = HttpResponse(t.render(c), mimetype=mimetype)
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
    return response
