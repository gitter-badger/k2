"""
Signals relating to stories.
"""
from django.dispatch import Signal

# Sent just before a story will be posted (after it's been approved and
# moderated; this can be used to modify the story (in place) with posting
# details or other such actions. If any receiver returns False the story will be
# discarded and a 403 (not allowed) response. This signal is sent at more or less
# the same time (just before, actually) as the Story object's pre-save signal,
# except that the HTTP request is sent along with this signal.
story_will_be_posted = Signal(providing_args=["story", "request"])

# Sent just after a story was posted. See above for how this differs
# from the Story object's post-save signal.
story_was_posted = Signal(providing_args=["story", "request"])

# Sent after a story was added to watched list.
story_was_watched = Signal(providing_args=["story", "request"])

# Sent after a story was "flagged" in some way. Check the flag to see if this
# was a user requesting removal of a story, a moderator approving/removing a
# story, or some other custom user flag.
story_was_flagged = Signal(providing_args=["story", "flag", "created", "request"])
