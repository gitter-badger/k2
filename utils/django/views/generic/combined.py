from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.views.generic.create_update import apply_extra_context, get_model_and_form_class, redirect

from create_update import get_current_user_form_class

def create_object_detail(request, queryset, current_user=True, object_id=None, slug=None,
        slug_field='slug', create_model=None, template_name=None, template_name_field=None,
        template_loader=loader, extra_context=None, post_save_redirect=None, login_required=False,
        context_processors=None, template_object_name='object',
        mimetype=None, form_class=None):
    """
    Generic detail of an object with create form for other model.

    Templates: ``<app_label>/<model_name>_detail_<create_model_name>_form.html``
    Context:
        object
            the object
    """
    if extra_context is None: extra_context = {}
    if (login_required or current_user) and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    
    create_model, form_class = get_model_and_form_class(create_model, form_class)
    
    if current_user:
        form_class = get_current_user_form_class(form_class, request.user.id)
    
    # create_object part
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save()

            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": create_model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class()
    
    # object_detail part
    model = queryset.model
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError("Generic detail view must be called with either an object_id or a slug/slug_field.")
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404("No %s found matching the query" % (model._meta.verbose_name))
    
    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_detail_%s_form.html" % (model._meta.app_label, model._meta.object_name.lower(), create_model._meta.object_name.lower())
    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        template_object_name: obj,
        'form': form,
    }, context_processors)
    apply_extra_context(extra_context, c)
    response = HttpResponse(t.render(c), mimetype=mimetype)
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
    return response
