from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from k2.stories.models import Story, Save, Watch

from stories import story_list
from utils import confirmation_view

def saved_list(request, queryset, **kwargs):
    queryset = queryset.filter(saved__in=[request.user])
    return story_list(request, queryset, **kwargs)

def watched_list(request, queryset, **kwargs):
    queryset = queryset.filter(watched__in=[request.user])
    return story_list(request, queryset, **kwargs)

# The following functions actually perform the various check/uncheck
# actions. They've been broken out into seperate functions to that they
# may be called from admin actions.

def perform_check(request, model, object_id):
    """
    Actually perform the checking of a story from a request.
    """
    story = get_object_or_404(Story, pk=object_id)
    model.objects.get_or_create(story=story, user=request.user)

def perform_uncheck(request, model, object_id):
    """
    Actually perform the unchecking of a story from a request.
    """
    story = get_object_or_404(Story, pk=object_id)
    get_object_or_404(model, story=story, user=request.user).delete()

# Confirmation views.
check_save = confirmation_view(
    model = Save,
    perform_func = perform_check,
    message = _("The %(verbose_name)s was created successfully."),
    doc = 'Displays a "story was saved" success message.'
)

uncheck_save = confirmation_view(
    model = Save,
    perform_func = perform_uncheck,
    message = _("The %(verbose_name)s was deleted."),
    doc = 'Displays a "story was unsaved" success message.'
)

check_watch = confirmation_view(
    model = Watch,
    perform_func = perform_check,
    message = _("The %(verbose_name)s was created successfully."),
    doc = 'Displays a "story was watched" success message.'
)

uncheck_watch = confirmation_view(
    model = Watch,
    perform_func = perform_uncheck,
    message = _("The %(verbose_name)s was deleted."),
    doc = 'Displays a "story was unwatched" success message.'
)
