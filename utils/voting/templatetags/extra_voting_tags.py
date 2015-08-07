from django import template

from ..models import Vote

register = template.Library()

class VotesForObjectNode(template.Node):
    def __init__(self, object, context_var, method='positive', count=True):
        self.object = object
        self.context_var = context_var
        self.method = method
        self.count = count

    def render(self, context):
        try:
            object = template.resolve_variable(self.object, context)
        except template.VariableDoesNotExist:
            return ''
        result = getattr(Vote.objects, '%s_for_object' % self.method)(object)
        if self.count:
            result = result.count()
        context[self.context_var] = result
        return ''

def do_votes_for_object(parser, token):
    """
    Retrieves the total score for an object and the number of votes
    it's received and stores them in a context variable which has
    ``score`` and ``num_votes`` properties.

    Example usage::

        {% votes_positive_for_object widget as votes %}
        {% votes_negative_for_object widget as votes %}
        {% num_votes_positive_for_object widget as votes %}
        {% num_votes_negative_for_object widget as votes %}

        {% foreach vote in votes %}{{ vote.user }}{% endfor %}
    """
    bits = token.contents.split()
    count = False
    method = 'negative'
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    if 'num' in bits[0]:
        count = True
    if 'positive' in bits[0]:
        method = 'positive'
    return VotesForObjectNode(bits[1], bits[3], method=method, count=count)

register.tag('votes_positive_for_object', do_votes_for_object)
register.tag('votes_negative_for_object', do_votes_for_object)
register.tag('num_votes_positive_for_object', do_votes_for_object)
register.tag('num_votes_negative_for_object', do_votes_for_object)
