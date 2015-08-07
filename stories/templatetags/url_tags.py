from urlparse import urlparse

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def url_domain(url):
    try:
        return urlparse(url)[1]
    except:
        return url

@stringfilter
@register.filter(name='domain')
def domain(url):
    try:
        return urlparse(url)[1]
    except:
        return url
