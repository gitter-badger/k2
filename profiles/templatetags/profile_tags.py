from django import template

from k2.profiles.models import GENDER_CHOICES

register = template.Library()

@register.filter
def gender(value):
    "Converts an into into gender string"
    try:
        genders = dict(GENDER_CHOICES)
        return genders[value]
    except KeyError:
        raise template.TemplateSyntaxError, \
            "%r tag requires an argument to be integer" % \
            token.contents.split()[0]

