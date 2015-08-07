from django.core.validators import EmailValidator, email_re
from django.utils.translation import ugettext as _

validate_jabber = EmailValidator(email_re, _(u'Enter a valid jabber ID.'), 'invalid')
