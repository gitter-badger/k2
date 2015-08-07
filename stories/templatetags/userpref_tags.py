from django import template

from k2.stories.models import UserPref

register = template.Library()

def sort_list(context, list_type='popular'):
    sort = context['request'].session.get('%s_sort' %list_type)
    return {'sort': sort, 'list_type': list_type}

@register.inclusion_tag('stories/templatetags/sort_list.html', takes_context=True)
def popular_sort_list(context):
    return sort_list(context)

@register.inclusion_tag('stories/templatetags/sort_list.html', takes_context=True)
def upcoming_sort_list(context):
    return sort_list(context, list_type='upcoming')

