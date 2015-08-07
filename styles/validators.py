import re

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

width_re = re.compile(r'^(\d+px)|(\d+%)|(auto)$')
validate_width = RegexValidator(width_re, _(u'Enter a valid width value.'), 'invalid')
