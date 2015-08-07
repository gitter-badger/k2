from django.db.models.fields import EmailField
from django.utils.translation import ugettext as _

from south.modelsinspector import add_introspection_rules

from ....core import validators

class JabberField(EmailField):
    default_validators = [validators.validate_jabber]
    description = _("Jabber ID")

add_introspection_rules([], ["^k2\.utils\.django\.db\.models\.fields\.JabberField"])
