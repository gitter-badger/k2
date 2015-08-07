'''
Created on 2010-08-19

@author: Artur Maciag <maciag.artur@gmail.com>
'''
from django import template
from django import db

from k2.stories.models import Category

register = template.Library()

@register.inclusion_tag('stories/templatetags/category_list.html', takes_context=True)
def category_list(context):
    categories = Category.objects.get_tree()
    return {'categories': categories}
