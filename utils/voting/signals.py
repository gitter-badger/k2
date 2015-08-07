"""
Signals relating to comments.
"""
from django.dispatch import Signal

# Sent just before a vote will be saved
vote_will_be_saved = Signal(providing_args=["vote", "obj", "request"])

# Sent just after a vote was saved. See above for how this differs
# from the Vote object's post-save signal.
vote_was_saved = Signal(providing_args=["vote", "obj", "request"])
