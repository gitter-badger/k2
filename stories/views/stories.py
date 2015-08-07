from django.views.generic.list_detail import object_list, object_detail
from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib import messages

from k2.utils.django.core.urlresolvers import reverse
from k2.utils.django.views.generic.create_update import create_object
from k2.utils.voting.views import vote_on_object

from k2.stories.models import SORT_CHOICE_POPULAR, SORT_CHOICE_NEW, \
    SORT_CHOICE_COMMENTED, Story, Category
from k2.stories import signals
from k2.profiles.models import USERCLASS_CHOICE_ROOKIE
from utils import check_url

def story_detail(request, queryset, **kwargs):
    # add user fields
    queryset = Story.objects.annotate_user(queryset, request.user.id)
    # We must filter here for further registration check
    if kwargs['object_id']:
        queryset = queryset.filter(pk=kwargs['object_id'])
    elif kwargs['slug'] and kwargs['slug_field']:
        queryset = queryset.filter(**{kwargs['slug_field']: kwargs['slug']})
    try:
        obj = queryset.get()
    except Story.DoesNotExist:
        raise Http404("No %s found matching the query" % str(queryset.model._meta.verbose_name))
    # signal that story was watched
    if request.user.is_authenticated():
        signals.story_was_watched.send(
            sender  = obj.__class__,
            story = obj,
            request = request
        )
    # If registration is required for accessing this story, and the user isn't
    # logged in, redirect to the login page.
    elif obj.registration_required:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    return object_detail(request, queryset, **kwargs)

def story_list(request, queryset, list_type, **kwargs):
    from datetime import datetime, timedelta
    
    sort = request.session.get('%s_sort' % list_type)
    try:
        random_story = queryset.filter(created_date__lte=datetime.now()-timedelta(days=1)).order_by('?')[0]
    except IndexError:
        random_story = None
    kwargs.setdefault('extra_context', {}).update({'random_story': random_story})
    if sort == SORT_CHOICE_POPULAR:
        queryset = queryset.order_by('-num_votes_positive')
    if sort == SORT_CHOICE_NEW:
        queryset = queryset.order_by('-published_date', '-created_date')
    if sort == SORT_CHOICE_COMMENTED:
        queryset = queryset.order_by('-num_comments')
    # add user fields
    queryset = Story.open.annotate_user(queryset, request.user.id)
    return object_list(request, queryset, **kwargs)

def category_list(request, queryset, **kwargs):
    slug = kwargs.pop('slug', None)
    category = Category.objects.get_or_none(slug=slug)
    if not category:
        raise Http404
    kwargs.setdefault('extra_context', {}).update({'category': category})
    queryset = queryset.filter(category=category)
    return story_list(request, queryset, **kwargs)

def search_list(request, queryset, **kwargs):
    query = request.GET.get('q', '')
    if query:
        # search
        queryset = Story.open.search(queryset, query)
        # add user fields
        queryset = Story.open.annotate_user(queryset, request.user.id)
        kwargs.setdefault('extra_context', {}).update({'search_query': query})
    else:
        queryset = Story.objects.none()
    return object_list(request, queryset, **kwargs)

def domain_object_list(request, queryset, domain, **kwargs):
    # search
    queryset = queryset.filter(url__icontains=domain)
    # add user fields
    queryset = Story.open.annotate_user(queryset, request.user.id)
    kwargs.setdefault('extra_context', {}).update({'domain': domain})
    return object_list(request, queryset, **kwargs)

def create_story(request, **kwargs):
    if request.method == 'GET' and 'url' in request.GET:
        try:
            url, title = check_url(request.GET['url'])
            kwargs.setdefault('extra_context', {}).update({'parsed_url': url, 'parsed_title': title,})
        except IOError, e:
            messages.error(request, _(str(e)), fail_silently=True)
    return create_object(request, pre_save_signal=signals.story_will_be_posted, \
        post_save_signal=signals.story_was_posted, signal_kwarg_name='story', **kwargs)

def dig_story(request, **kwargs):
    kwargs.update({'karma': request.user.profile.get_vote_weight(),})
    return vote_on_object(request, **kwargs)

def bury_story(request, **kwargs):
    kwargs.update({'karma': -1*request.user.profile.get_vote_weight(),})
    return vote_on_object(request, **kwargs)