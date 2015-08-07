from django.conf import settings

# Stories
#
# How long story can be in upcoming list (in days)
STORY_LIFE_TIME = getattr(settings, 'STORY_LIFE_TIME', 2)
# Edit time (in minutes)
STORY_EDIT_TIME = getattr(settings, 'STORY_EDIT_TIME', 15)
# karma required to promote story to popular list
STORY_TRESHOLD  = getattr(settings, 'STORY_TRESHOLD', 20)
STORY_THUMB_DIR = getattr(settings, 'THUMB_DIR', 'img/thumbs/')

# Comments in stories
COMMENT_EDIT_TIME = getattr(settings, 'COMMENT_EDIT_TIME', 15) # in mins
