from django import template
from django.conf import settings
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.contrib import messages

from k2.stories.views.utils import msg_confirmation_view
from k2.stories.models import Story, StoryFlag
from k2.stories import signals

@csrf_protect
@require_GET
@login_required
def flag(request, story_id, next=None):
    """
    Flags a story. Action on GET.
    """
    story = get_object_or_404(Story, pk=story_id)

    # Flag the story as approved.
    perform_flag(request, story)
    
    return flag_done(request, next, story)

@csrf_protect
@require_GET
@permission_required("stories.can_moderate")
def delete(request, story_id, next=None):
    """
    Deletes a story. Action on GET. Requires the "can
    moderate stories" permission.
    """
    story = get_object_or_404(Story, pk=story_id)

    # Flag the story as deleted instead of actually deleting it.
    perform_delete(request, story)
    
    return delete_done(request, next, story)

@csrf_protect
@require_GET
@permission_required("stories.can_moderate")
def approve(request, story_id, next=None):
    """
    Approve a comment (that is, mark it as public and non-removed). Action
    on GET. Requires the "can moderate stories" permission.
    """
    story = get_object_or_404(Story, pk=story_id)

    # Flag the story as approved.
    perform_approve(request, story)
    
    return approve_done(request, next, story)

@csrf_protect
@require_GET
@permission_required("stories.can_moderate")
def lock(request, story_id, next=None):
    """
    Approve a comment (that is, mark it as public and non-removed). Action
    on GET. Requires the "can moderate stories" permission.
    """
    story = get_object_or_404(Story, pk=story_id)

    # Flag the story as approved.
    perform_lock(request, story)
    
    return lock_done(request, next, story)

# The following functions actually perform the various flag/aprove/delete
# actions. They've been broken out into seperate functions to that they
# may be called from admin actions.

def perform_flag(request, story):
    """
    Actually perform the flagging of a story from a request.
    """
    flag, created = StoryFlag.objects.get_or_create(
        story   = story,
        user    = request.user,
        flag    = StoryFlag.SUGGEST_REMOVAL
    )
    signals.story_was_flagged.send(
        sender  = story.__class__,
        story   = story,
        flag    = flag,
        created = created,
        request = request,
    )

def perform_delete(request, story):
    flag, created = StoryFlag.objects.get_or_create(
        story   = story,
        user    = request.user,
        flag    = StoryFlag.MODERATOR_DELETION
    )
    story.is_removed = True
    story.save()
    signals.story_was_flagged.send(
        sender  = story.__class__,
        story   = story,
        flag    = flag,
        created = created,
        request = request,
    )


def perform_approve(request, story):
    flag, created = StoryFlag.objects.get_or_create(
        story   = story,
        user    = request.user,
        flag    = StoryFlag.MODERATOR_APPROVAL,
    )

    story.is_removed = False
    story.is_public = True
    story.save()

    signals.story_was_flagged.send(
        sender  = story.__class__,
        story   = story,
        flag    = flag,
        created = created,
        request = request,
    )

def perform_lock(request, story):
    flag, created = StoryFlag.objects.get_or_create(
        story   = story,
        user    = request.user,
        flag    = StoryFlag.MODERATOR_LOCK,
    )

    story.is_removed = False
    story.is_public = False
    story.is_locked = True
    story.save()

    signals.story_was_flagged.send(
        sender  = story.__class__,
        story   = story,
        flag    = flag,
        created = created,
        request = request,
    )

# Confirmation views.
flag_done = msg_confirmation_view(
    message = _("Thanks for taking the time to improve the quality of discussion on our site"),
    message_func = messages.success,
    doc = 'Displays a "story was flagged" message.'
)

delete_done = msg_confirmation_view(
    message = _("Thanks for taking the time to improve the quality of discussion on our site"),
    message_func = messages.success,
    doc = 'Displays a "story was deleted" message.'
)

approve_done = msg_confirmation_view(
    message = _("Thanks for taking the time to improve the quality of discussion on our site"),
    message_func = messages.success,
    doc = 'Displays a "story was approved" message.'
)

lock_done = msg_confirmation_view(
    message = _("Thanks for taking the time to improve the quality of discussion on our site"),
    message_func = messages.success,
    doc = 'Displays a "story was locked" message.'
)