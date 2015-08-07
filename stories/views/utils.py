# with statement in python 2.5
from __future__ import with_statement

import formatter
import urllib
import textwrap
from urlparse import urlparse

from django.http import HttpResponseRedirect
from django.contrib import messages

from k2.utils.htmlparse import TitleParser

def next_redirect(request, default):
    path = request.META.get('HTTP_REFERER', default)
    return HttpResponseRedirect(path)

def confirmation_view(model, perform_func, message, doc="Display a confirmation view."):
    """
    Confirmation view generator for the "story was
    checked/unchecked" views.
    """
    def confirmed(request, object_id):
        perform_func(request, model, object_id)
        messages.success(request, message  % \
                {"verbose_name": model._meta.verbose_name}, fail_silently=True)
        return next_redirect(request, '/')
    confirmed.__doc__ = textwrap.dedent("""\
        %s

        Context:
            story
                The checked story
        """ % doc
    )
    return confirmed

def msg_confirmation_view(message, message_func, doc="Display a confirmation view."):
    """
    Confirmation view generator for the "story was
    posted/edited/flagged/deleted/approved" views.
    """
    def confirmed(request, next, story, **msg_kwargs):
        message_func(request, message % msg_kwargs, fail_silently=True)
        return HttpResponseRedirect(story.get_absolute_url())
    confirmed.__doc__ = textwrap.dedent("""\
        %s

        Context:
            comment
                The posted comment
        """ % (doc)
    )
    return confirmed

def check_url(url):
    page = urlparse(url, 'http')
    if not page.netloc:
        raise IOError("Submitted URL address is invalid. Please correct it and try again.")
    else:
        url = page.geturl()
        try:
            data = urllib.urlopen(page.geturl())
            format = formatter.NullFormatter()
            with TitleParser(format) as parser:
                parser.feed(data.read())
                title = parser.get_title()
            data.close()
            return url, title
        except IOError:
            raise IOError("Unable to access this content, please check the URL and try again.")