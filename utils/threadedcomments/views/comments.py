from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib import comments
from django.contrib.comments.views.comments import post_comment as django_post_comment
from django.contrib.comments.views.utils import confirmation_view
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.contrib import messages

from utils import msg_confirmation_view

@csrf_protect
@require_POST
def post_comment(request, *args, **kwargs):
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not request.user.get_full_name() == request.POST['name']:
            # name field spoofed!
            data['name'] = request.user.get_full_name() or request.user.username
        if not request.user.email == request.POST['email']:
            # email field spoofed!
            data['email'] = request.user.email
        if not data.get('url', '') and request.user.get_profile().website:
            data["url"] = request.user.get_profile().website
    request.POST = data
    return django_post_comment(request, *args, **kwargs)
@csrf_protect
def edit(request, comment_id, next=None):
    """
    Edits a comment. Confirmation on GET, action on POST. Requires the "can
    moderate comments" permission.

    Templates: `comments/edit.html`,
    Context:
        comment
            the flagged `comments.comment` object
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()

    # Check if fields spoofed
    if request.method == 'POST' and request.user.is_authenticated():
        if not request.user.get_full_name() == request.POST['name']:
            # name field spoofed!
            data['name'] = request.user.get_full_name() or request.user.username
        if not request.user.email == request.POST['email']:
            # email field spoofed!
            data['email'] = request.user.email
        if not data.get('url', '') and request.user.get_profile().website:
            data["url"] = request.user.get_profile().website

    # Check to see if the POST data overrides the view's next argument.
    next = data.get("next", next)

    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)
    
    # Check editor is an author
    if not comment.user == request.user:
        raise Http404

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    # @todo: comment form with instance param
    form = comments.get_form()(comment.content_object, data=data)

    # Edit on POST
    if request.method == 'POST':
        # If there are errors or if we requested a preview show the comment
        if form.errors or preview:
            template_list = [
                # These first two exist for purely historical reasons.
                # Django v1.0 and v1.1 allowed the underscore format for
                # preview templates, so we have to preserve that format.
                "comments/%s_%s_preview.html" % (model._meta.app_label, model._meta.module_name),
                "comments/%s_preview.html" % model._meta.app_label,
                # Now the usual directory based template heirarchy.
                "comments/%s/%s/preview.html" % (model._meta.app_label, model._meta.module_name),
                "comments/%s/preview.html" % model._meta.app_label,
                "comments/preview.html",
            ]
            return render_to_response(
                template_list, {
                    "comment" : form.data.get("comment", ""),
                    "form" : form,
                    "next": next,
                },
                RequestContext(request, {})
            )

        # Otherwise edit the comment
        comment = form.get_comment_object()
        perform_edit(request, comment)

        return edit_done(request, next, comment, name=force_unicode(comment._meta.verbose_name), obj=force_unicode(obj))

    # Render a form on GET
    else:
        return render_to_response('comments/edit.html',
            {'form': form, 'comment': comment, 'object': comment.content_object, "next": next},
            RequestContext(request)
        )

# The following functions actually perform the various flag/aprove/delete
# actions. They've been broken out into seperate functions to that they
# may be called from admin actions.

def perform_edit(request, comment):
    """
    Actually perform the flagging of a comment from a request.
    """
    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_edited.send(
        sender  = comment.__class__,
        comment = comment,
        request = request,
    )

# Confirmation views.

#comment_done = confirmation_view(
#    template = "comments/posted.html",
#    doc = """Display a "comment was posted" success page."""
#)

edit_done = msg_confirmation_view(
    message = _("The %(name)s \"%(obj)s\" was changed successfully."),
    message_func = messages.success,
    doc = 'Displays a "comment was edited" success page.'
)
