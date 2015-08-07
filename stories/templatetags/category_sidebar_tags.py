from django import template

from k2.stories.models import Category

register = template.Library()

@register.inclusion_tag('stories/templatetags/sidebar_category_info.html', takes_context=True)
def sidebar_category_info(context):
    try:
        category = context['category']
    except KeyError:
        category = None
    return {'category': category,}