from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import flatpage as flatpage_detail
from django.contrib.sites.models import Site
from django.contrib import messages
from django.template import loader, RequestContext
#from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _

from ...shortcuts import get_object_or_none
from forms import FlatPageEditForm

DEFAULT_TEMPLATE = 'flatpages/default_form.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
@csrf_protect
def flatpage(request, url):
    """
    Extended editable flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not request.GET.get('action') in ('create', 'edit', 'delete'):
        return flatpage_detail(request, url)
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_none(FlatPage, url__exact=url, sites__id__exact=settings.SITE_ID)
    if not f:
        if not request.user.has_perm('flatpages.add_flatpage'):
            raise Http404
        f = FlatPage(url=url)
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f and f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if request.method == 'POST':
        form = FlatPageEditForm(request.POST, instance=f)
        if form.is_valid(): # All validation rules pass
            f.save()
            current_site = Site.objects.get_current()
            if not current_site in f.sites.all():
                # Assign page to current site
                f.sites.add(current_site)
                f.save()
            msg = _("The %(verbose_name)s was updated successfully.") %\
                {"verbose_name": FlatPage._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(f.url)
    else:
        if request.GET.get('action') == 'delete':
            f.delete()
            msg = _("The %(verbose_name)s was deleted.") %\
                {"verbose_name": FlatPage._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect('/')
        form = FlatPageEditForm(instance=f)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    c = RequestContext(request, {
        'form': form,
        'flatpage': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FlatPage, f.id)
    return response
