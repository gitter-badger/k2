from datetime import datetime

from k2.utils.voting import signals as voting_signals

from k2.stories import signals
from k2.stories.models import Watch, Story
from k2.stories import settings as story_settings

def update_watched(sender, story, request, **kwargs):
    """Updates last_leen in Watch"""
    try:
        Watch.objects.filter(story=story, user=request.user).update(last_seen=datetime.now())
    except Watch.DoesNotExist:
        pass

def promote(sender, vote, obj, request, **kwargs):
    """Promotes stories from upcoming to popular"""
    if isinstance(obj, Story) and not obj.published_date:
        try:
            story = Story.objects.all(with_karma=True).get(pk=obj.id)
            if story.karma >= story_settings.STORY_TRESHOLD:
                # We got enough karma to promote
                story.published_date = datetime.now()
                story.save()
        except Story.DoesNotExist:
            pass

signals.story_was_watched.connect(update_watched,
    dispatch_uid = "k2.stories.update_watched")
voting_signals.vote_was_saved.connect(promote,
    dispatch_uid = "k2.stories.promote")
