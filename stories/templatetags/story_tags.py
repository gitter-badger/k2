from django import template
from django.core.cache import cache
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User

from threadedcomments.models import ThreadedComment

from k2.utils.voting.models import Vote
from k2.utils.voting.forms import ObjectVoteForm

from k2.stories.models import Story
from k2.stories.forms import SubmitStoryForm, SubmitReferenceForm

register = template.Library()

class StoryUrlNode(template.Node):
    def __init__(self, story):
        self.story = story
    def render(self, context):
        story = template.Variable(self.story).resolve(context)
        user = context['request'].user
        if user.is_authenticated() and user.get_pref().frame:
            return story.frame_url
        return story.url

@register.tag
def story_url(parser, token):
    try:
        tag, story = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return StoryUrlNode(story)

@register.inclusion_tag('stories/templatetags/story_detail.html', takes_context=True)
def render_story_detail(context, story):
    request = context['request']
    perms = context['perms']
    if not hasattr(story, 'num_votes_positive'):
        story.num_votes_positive = Vote.objects.positive_for_object(story).count()
    return {'request': request, 'story': story, 'perms': perms}

@register.inclusion_tag('stories/templatetags/story.html', takes_context=True)
def render_story(context, story):
    return render_story_detail(context, story)

@register.inclusion_tag('stories/templatetags/story_random.html', takes_context=True)
def render_story_random(context, story):
    return render_story_detail(context, story)

@register.inclusion_tag('stories/templatetags/story_simple.html', takes_context=True)
def render_story_simple(context, story):
    return render_story_detail(context, story)

@register.inclusion_tag('stories/templatetags/story_mini.html', takes_context=True)
def render_story_mini(context, story):
    return render_story_detail(context, story)

@register.inclusion_tag('stories/templatetags/comment.html', takes_context=True)
def render_comment(context, comment):
    request = context['request']
    perms = context['perms']
    """
    Render the comment (as returned by ``{% render_comment %}``) 
    through the ``stories/templatetags/comment.html`` template.

    Syntax::

        {% render_comment [comment] %}
    """
    return {'request': request, 'comment': comment, 'perms': perms}

@register.inclusion_tag('stories/templatetags/comment_simple.html', takes_context=True)
def render_comment_simple(context, comment):
    """
    Render the comment (as returned by ``{% render_comment_simple %}``) 
    through the ``stories/templatetags/comment_simple.html`` template.

    Syntax::

        {% render_comment_simple [comment] %}
    """
    return render_comment(context, comment)

@register.inclusion_tag('stories/templatetags/reference.html', takes_context=True)
def render_reference(context, reference):
    request = context['request']
    perms = context['perms']
    """
    Render the reference (as returned by ``{% render_reference %}``) 
    through the ``stories/templatetags/reference.html`` template.

    Syntax::

        {% render_reference [reference] %}
    """
    return {'request': request, 'reference': reference, 'perms': perms}

@register.inclusion_tag('stories/templatetags/comment_detail_simple.html', takes_context=True)
def comment_detail_simple(context, comment, obs):
    return comment_detail(context, comment, obs)
    
@register.inclusion_tag('stories/templatetags/story_submit_form.html', takes_context=True)
def render_story_submit_form(context):
    request = context['request']
    form = SubmitStoryForm()
    return {'request': request, 'form': form}

@register.inclusion_tag('stories/templatetags/reference_submit_form.html', takes_context=True)
def render_reference_submit_form(context, story):
    request = context['request']
    form = SubmitReferenceForm()
    return {'request': request, 'story': story, 'form': form}

@register.inclusion_tag('stories/templatetags/site_stats.html', takes_context=True)
def render_site_stats(context):
    request = context['request']
    users_cached = cache.get('users_online', {})
    users_online = users_cached and User.objects.filter(id__in = users_cached.keys()) or []
    guests_cached = cache.get('guests_online', {})
    guests_online = guests_cached or []
    stories = Story.objects.all().count()
    comments = Comment.objects.all().count()
    users = User.objects.all().count()
    return {'request': request, 'users_online': users_online, 'guests_online': guests_online,
        'users_count': len(users_online), 'guests_count': len(guests_online), 
        'stories': stories, 'comments': comments, 'users': users}
