import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.contrib import comments
from django.contrib.comments import moderation
from django.db.models import Model
from django.template import Context, loader

class RelatedModerator(moderation.CommentModerator):
    """
    Handles moderation of a set of models.

    Designed to moderate classes with foreign key relation instead of generic.
    Override attributes::
    
    ``pre_save_signal``
        Signal to pre-save moderation. Default value is ``None`` 
        and must be changed.

    ``post_save_signal``
        Signal to post-save moderation. Default value is ``None`` 
        and must be changed.

    ``related_field``
        Set this to field name in related class which has relation with moderated class. 
        Default value is ``site``.
        
    ``related_class``
        Set this to related class which has relation with moderated class. 
        Default value is ``Comment``.
    """
    pre_save_signal = None
    post_save_signal = None
    related_field = 'site'
    related_class = comments.get_model()

    def __init__(self, model):
        self._model = model
        self._registry = {}
        self.connect()

    def email(self, related_object, content_object, request):
        """
        Send email notification of a new related object to site staff when email
        notifications have been requested.

        Templates: ``<app_label>/<model_name>_notification_email.txt``
        Context:
            related_object
                the object
        """
        if not self.email_notification:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        t = loader.get_template('%s/%s_notification_email.txt' % (related_object._meta.app_label, related_object._meta.object_name.lower()))
        c = Context({ 'related_object': related_object,
                      'content_object': content_object })
        subject = '[%s] New %s posted on "%s"' % (Site.objects.get_current().name,
                                        related_object._meta.object_name.lower(), content_object)
        message = t.render(c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

    def connect(self):
        """
        Hook up the moderation methods to pre- and post-save signals
        from the objects models.

        """
        if not self.pre_save_signal or not self.post_save_signal:
            raise ValueError("Cannot connect to signals because pre_save_signal or post_save_signal is not set")
        self.pre_save_signal.connect(self.pre_save_moderation, sender=self.related_class)
        self.post_save_signal.connect(self.post_save_moderation, sender=self.related_class)

    def pre_save_moderation(self, sender, related_object, request, **kwargs):
        """
        Apply any necessary pre-save moderation steps to new
        objects.

        """
        content_object = getattr(related_object, self.related_field)
        if not isinstance(content_object, Model):
            raise ValueError("The field '%s' is not related to Model class" % self.related_field)
        model = content_object.__class__
        if model not in self._registry:
            return
        moderation_class = self._registry[model]

        # Object will be disallowed outright (HTTP 403 response)
        if not moderation_class.allow(related_object, content_object, request): 
            return False

        if moderation_class.moderate(related_object, content_object, request):
            related_object.is_public = False

    def post_save_moderation(self, sender, related_object, request, **kwargs):
        """
        Apply any necessary post-save moderation steps to new
        objects.

        """
        content_object = getattr(related_object, self.related_field)
        if not isinstance(content_object, Model):
            raise ValueError("The field '%s' is not related to Model class" % self.related_field)
        model = content_object.__class__
        if model not in self._registry:
            return
        self._registry[model].email(related_object, content_object, request)