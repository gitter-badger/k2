from django.contrib import comments
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.comments.views.moderation import perform_flag, perform_delete, perform_approve
from django.contrib.comments.views.utils import next_redirect, confirmation_view
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.contrib import messages

from k2.utils.threadedcomments import signals

from utils import msg_confirmation_view

@csrf_protect
@require_GET
@login_required
def flag(request, comment_id, next=None):
    """
    Flags a comment. Action on GET.

    Context:
        comment
            the flagged `comments.comment` object
    """
    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    # Flag the comment as approved.
    perform_flag(request, comment)
    
    return flag_done(request, next, comment)
@csrf_protect
@require_GET
@permission_required("comments.can_moderate")
def delete(request, comment_id, next=None):
    """
    Deletes a comment. Action on GET. Requires the "can
    moderate comments" permission.

    Context:
        comment
            the flagged `comments.comment` object
    """
    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    perform_delete(request, comment)

    return delete_done(request, next, comment)
@csrf_protect
@require_GET
@permission_required("comments.can_moderate")
def approve(request, comment_id, next=None):
    """
    Approve a comment (that is, mark it as public and non-removed). Action
    on GET. Requires the "can moderate comments" permission.

    Context:
        comment
            the `comments.comment` object for approval
    """
    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    # Flag the comment as approved.
    perform_approve(request, comment)
    
    return approve_done(request, next, comment)

# Confirmation views.

flag_done = msg_confirmation_view(
    message = _("Thanks for taking the time to improve the quality of discussion on our site"),
    message_func = messages.success,
    doc = 'Displays a "comment was flagged" message.'
)

delete_done = msg_confirmation_view(
    message = _("Thanks for removing"),
    message_func = messages.success,
    doc = 'Displays a "comment was deleted" message.'
)

approve_done = msg_confirmation_view(
    message = _("Thanks for approving"),
    message_func = messages.success,
    doc = 'Displays a "comment was approved" message.'
)