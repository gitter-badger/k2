import re

from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy

def strip_spaces_between_tags(value):
    """Returns the given HTML with spaces between tags removed."""
    value = re.sub(r'^\s+', '', force_unicode(value)) # Replace all lines with spaces only at the beginning of document
    value = re.sub(r'\n\s+', '\n', force_unicode(value)) # Replace all leading spaces at the beginning of a line
    return re.sub(r'>\s+<', '><', force_unicode(value))
strip_spaces_between_tags = allow_lazy(strip_spaces_between_tags, unicode)
