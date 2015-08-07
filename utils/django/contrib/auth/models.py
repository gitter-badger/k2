from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User, Group, UserManager
from django.db import models

class SitePrefNotAvailable(Exception):
    pass

class AdminManager(UserManager):
    """
    Custom manager for the User model.
    """
    def get_query_set(self):
        """
        Overwrites the get_query_set to only return Users in the queue.
        """
        return super(AdminManager, self).get_query_set().filter(userprofile__queue=True)

def in_group_id(self, group_id):
    if not hasattr(self, '_group_ids_cache'):
        self._group_ids_cache = [g.id for g in self.groups.all()]
    return group_id in self._group_ids_cache

def is_administrator(self):
    if not hasattr(self, '_is_administrator_cache'):
        self._is_administrator_cache = self.in_group_id(settings.ADMIN_GROUP_ID)
    return self._is_administrator_cache

def is_moderator(self):
    if not hasattr(self, '_is_moderator_cache'):
        self._is_moderator_cache = self.is_administrator() or self.in_group_id(settings.MOD_GROUP_ID)
    return self._is_moderator_cache

def is_banned(self):
    if not hasattr(self, '_is_banned_cache'):
        self._is_banned_cache = self.in_group_id(settings.BANNED_GROUP_ID)
    return self._is_banned_cache

def get_pref(self):
    """
    Returns site-specific preferences for this user. Raises
    SitePrefNotAvailable if this site does not allow profiles.
    """
    if not hasattr(self, '_pref_cache'):
        from django.conf import settings
        if not getattr(settings, 'AUTH_PREF_MODULE', False):
            raise SitePrefNotAvailable('You need to set AUTH_PREF_MO'
                                            'DULE in your project settings')
        try:
            app_label, model_name = settings.AUTH_PREF_MODULE.split('.')
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
            self._pref_cache, created = model._default_manager.using(self._state.db).get_or_create(user=self)
            self._pref_cache.user = self
        except (ImportError, ImproperlyConfigured):
            raise SitePrefNotAvailable
    return self._pref_cache

