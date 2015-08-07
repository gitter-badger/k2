"Styles' userstyle templatetags module"
try:
    from compress.templatetags import compressed
except ImportError:
    compressed = None

from django import template

from k2.styles import get_style_list, settings

def render(name, rel='alternate stylesheet', media='screen, projection'):
    return  u'<link rel="%s" title="%s" href="%s%s/%s.css" media="%s">' % (rel, name, settings.STYLES_URL, name, name, media)

def render_compressed(name):
    node = compressed.CompressedCSSNode(name)
    return node.render({name:name})

register = template.Library()

@register.tag
def userstyle(parser, token):
    return UserStyleNode()

@register.tag
def altstyles(parser, token):
    return AltStylesNode()

@register.tag
def max_width(parser, token):
    return AltStylesNode()

class UserStyleNode(template.Node):
    def render(self, context):
        style = template.Variable("userstyle").resolve(context)
        if compressed:
            return render_compressed(style)
        else:
            return render(style, 'stylesheet')

class AltStylesNode(template.Node):
    def render(self, context):
        style = template.Variable("userstyle").resolve(context)
        if compressed:
            return "\r\n".join(map(render_compressed, get_style_list()))
        else:
            return "\r\n".join(map(render, get_style_list()))

class MaxWidthNode(template.Node):
    def render(self, context):
        style = template.Variable("userstyle").resolve(context)
        if compressed:
            return "\r\n".join(map(render_compressed, get_style_list()))
        else:
            return "\r\n".join(map(render, get_style_list()))

