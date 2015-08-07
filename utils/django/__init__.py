def InstallDjangoShotrcuts():
    from django.db.models.manager import Manager
    from shortcuts import get_object_or_none
    Manager.get_or_none = get_object_or_none

def InstallDjangoAuthentication():
    from django.contrib.auth import models
    from contrib.auth.models import get_pref, in_group_id, is_administrator, is_moderator, \
        is_banned, AdminManager
    from contrib.auth import signals

    models.User.add_to_class('get_pref', get_pref)
    models.User.add_to_class('in_group_id', in_group_id)
    models.User.add_to_class('is_administrator', is_administrator)
    models.User.add_to_class('is_moderator', is_moderator)
    models.User.add_to_class('is_banned', is_banned)
    models.User.add_to_class('admin_objects', AdminManager())
    models.signals = signals
