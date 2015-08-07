from django.conf import settings
from django import template

from google_analytics.templatetags.analytics import AnalyticsNode

register = template.Library()

class EmptyAnalyticsNode(AnalyticsNode):
    def render(self, context):
        return ''

def do_get_analytics(parser, token):
    """
    Renders Google Analytics code only if DEBUG = False 
    and gets ID from settings.GOOGLE_ANALYTICS_ID when possible.
    """
    contents = token.split_contents()
    tag_name = contents[0]
    template_name = 'google_analytics/%s_template.html' % tag_name
    if len(contents) == 2:
        # split_contents() knows not to split quoted strings.
        code = contents[1]
        if not (code[0] == code[-1] and code[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
        code = code[1:-1]
    elif len(contents) == 1:
        code = getattr(settings, 'GOOGLE_ANALYTICS_ID', False)
    else:
        raise template.TemplateSyntaxError, "%r cannot take more than one argument" % tag_name
   
    if not code:
        current_site = Site.objects.get_current()
    else:
        current_site = None

    if getattr(settings, 'DEBUG', False):
        return EmptyAnalyticsNode(current_site, code, template_name)
    return AnalyticsNode(current_site, code, template_name)

register.tag('google_analytics', do_get_analytics)
register.tag('google_analytics_async', do_get_analytics)
