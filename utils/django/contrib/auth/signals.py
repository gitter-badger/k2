from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib.auth.models import User

class SitePrefNotAvailable(Exception):
    pass

def user_post_save(sender, instance, **kwargs):
    if not getattr(settings, 'AUTH_PREF_MODULE', False):
        raise SitePrefNotAvailable
    try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    except ValueError:
        raise SitePrefNotAvailable('app_label and model_name should'
            ' be separated by a dot in the AUTH_PREF_MODULE set'
            'ting')

    try:
        model = models.get_model(app_label, model_name)
        if model is None:
            raise SitePrefNotAvailable('Unable to load the preference '
                'model, check AUTH_PREF_MODULE in your project sett'
                'ings')
        # Auto-create
        profile, created = model.objects.get_or_create(user=instance)
        profile.user = instance
    except (ImportError, ImproperlyConfigured):
        raise SitePrefNotAvailable

models.signals.post_save.connect(user_post_save, sender=User)
