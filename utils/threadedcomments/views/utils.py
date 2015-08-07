import urllib
import textwrap

from django.http import HttpResponseRedirect
from django.contrib.comments.views.utils import next_redirect

def msg_confirmation_view(message, message_func, doc="Display a confirmation view."):
    """
    Confirmation view generator for the "comment was
    posted/edited/flagged/deleted/approved" views.
    """
    def confirmed(request, next, comment, **msg_kwargs):
        message_func(request, message % msg_kwargs, fail_silently=True)
        if comment.get_absolute_url():
            return HttpResponseRedirect(comment.get_absolute_url(anchor_pattern="#comment-%(id)s"))
        return next_redirect(request.POST.copy(), next, None, comment=comment.pk)
    confirmed.__doc__ = textwrap.dedent("""\
        %s

        Context:
            comment
                The posted comment
        """ % (doc)
    )
    return confirmed