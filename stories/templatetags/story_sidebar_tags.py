from datetime import timedelta, datetime

from django import template
from django.contrib.contenttypes.models import ContentType

from threadedcomments.models import ThreadedComment

from k2.utils.voting.models import Vote

from k2.stories.models import Story

register = template.Library()

@register.inclusion_tag('stories/templatetags/sidebar_top_stories.html', takes_context=True)
def sidebar_top_stories(context):
    request = context['request']
    perms = context['perms']
    now = datetime.now()
    stories = Story.open.all(with_num_votes=True, with_num_votes_positive=True, \
            with_num_votes_negative=True, with_num_comments=True, \
            with_num_references=True).exclude(published_date=None).order_by('-num_votes_positive')
    day = stories.filter(published_date__gte=now-timedelta(days=1))[:5]
    week = stories.filter(published_date__gte=now-timedelta(days=7))[:5]
    month = stories.filter(published_date__gte=now-timedelta(days=30))[:5]
    return {'request': request, 'perms': perms, 'day': day, 'week': week, 'month': month}

@register.inclusion_tag('stories/templatetags/sidebar_user_stories.html', takes_context=True)
def sidebar_user_stories(context):
    request = context['request']
    return {'request': request}

@register.inclusion_tag('stories/templatetags/sidebar_tag_cloud.html', takes_context=True)
def sidebar_tag_cloud(context):
    request = context['request']
    return {'request': request}

@register.inclusion_tag('stories/templatetags/sidebar_add_story.html', takes_context=True)
def sidebar_add_story(context):
    request = context['request']
    return {'request': request}

@register.inclusion_tag('stories/templatetags/sidebar_search.html', takes_context=True)
def sidebar_search(context):
    request = context['request']
    q = request.GET.get('q') or ''
    return {'request': request, 'q': q}

@register.inclusion_tag('stories/templatetags/sidebar_story_random_comment.html', takes_context=True)
def sidebar_story_random_comment(context, story_id):
    request = context['request']
    story = Story.objects.get(pk=story_id)
    try:
        comment = ThreadedComment.objects.for_model(story).select_related().order_by('?')[0]
    except IndexError:
        comment = None
    return {'request': request, 'comment': comment, 'observing': None}

@register.inclusion_tag('stories/templatetags/sidebar_story_votes_positive.html', takes_context=True)
def sidebar_story_votes_positive(context, story):
    request = context['request']
    ctype = ContentType.objects.get_for_model(story)
    votes = Vote.objects.select_related().filter(content_type=ctype, object_id=story._get_pk_val(), vote__gt=0)
    return {'request': request, 'story': story, 'votes': votes}

@register.inclusion_tag('stories/templatetags/sidebar_story_votes_negative.html', takes_context=True)
def sidebar_story_votes_negative(context, story):
    request = context['request']
    ctype = ContentType.objects.get_for_model(story)
    votes = Vote.objects.select_related().filter(content_type=ctype, object_id=story._get_pk_val(), vote__lt=0)
    return {'request': request, 'story': story, 'votes': votes}

@register.inclusion_tag('stories/templatetags/sidebar_story_author.html', takes_context=True)
def sidebar_story_author(context, user):
    request = context['request']
    return {'request': request, 'user': user}
