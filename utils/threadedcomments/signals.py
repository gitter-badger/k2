"""
Signals relating to comments.
"""
from django.dispatch import Signal

comment_was_edited = Signal(providing_args=["comment", "request"])
