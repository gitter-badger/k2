from django import template

register = template.Library()

class NavNode(template.Node):
    def __init__(self, page):
        self.page = page
    def render(self, context):
        context.update({'nav': {self.page: True}})
        return ''

def nav(parser, token):
    """
    Changes (or adds if necessary) nav variable in context.

    Sample usage::

        {% nav "home" %}
    """
    try:
        tag_name, page = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % tag_name
    if not (page[0] == page[-1] and page[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return NavNode(page[1:-1])
    
nav = register.tag(nav)