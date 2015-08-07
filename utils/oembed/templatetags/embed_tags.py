from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from oembed.models import StoredOEmbed
from oembed.consumer import OEmbedConsumer

register = template.Library()

@register.filter('embed')
@stringfilter
def embed_filter(input, args=None):
    if args:
        dimensions = args.lower().split('x')
        if len(dimensions) != 2:
            raise template.TemplateSyntaxError("OEmbed's optional WIDTHxHEIGH" \
                "argument requires WIDTH and HEIGHT to be positive integers.")
        width, height = map(int, dimensions)
    else:
        width = height = None

    client = OEmbedConsumer()
    parsed = client.parse(input, width, height)
    # @todo: find better solution to detect parsing results
    if client.extract(input, width, height):
        return mark_safe(parsed)
    return ''
embed_filter.is_safe = True

@register.filter('embedthumb')
@stringfilter
def embedthumb_filter(input, args=None):
    if args:
        dimensions = args.lower().split('x')
        if len(dimensions) != 2:
            raise template.TemplateSyntaxError("OEmbed's optional WIDTHxHEIGH" \
                "argument requires WIDTH and HEIGHT to be positive integers.")
        width, height = map(int, dimensions)
    else:
        width = height = None
    try:
        thumbnail = StoredOEmbed.objects.get(match=input, maxwidth=width, maxheight=height).thumbnail_url
        if not thumbnail:
            raise StoredOEmbed.DoesNotExist
        return render_to_string('embed/templatetags/thumb.html', { 'url': input, 'thumbnail': thumbnail, 'width': width, 'height': height })
    except:
        return ''
embedthumb_filter.is_safe = True
