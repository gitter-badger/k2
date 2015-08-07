from django.core.management.base import NoArgsCommand
from django.db import transaction, connection
from django.conf import settings
from django.contrib.auth.models import User, Group

# PHPDug groups
GROUP_ID_BANNED = 10
GROUP_ID_MOD = 3
GROUP_ID_ADMIN = 4

SQL = """
SELECT
    user_id,
    username,
    email,
    password,
    group_id,
    (SELECT CONVERT(date, DATETIME) FROM dug_ip AS ip WHERE ip.user_id = user_id ORDER BY date DESC LIMIT 1) AS last_login,
    CONVERT(created, DATETIME) AS date_joined
FROM dug_users;
"""

class Command(NoArgsCommand):
    help = "Migrates from phpdug to django"

    def handle(self, *args, **options):
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)

        cursor = connection.cursor()

        cursor.execute(SQL)
        banned_group, c = Group.objects.get_or_create(pk=settings.BANNED_GROUP_ID, name='banned')
        mods_group, c = Group.objects.get_or_create(pk=settings.MOD_GROUP_ID, name='mods')
        admins_group, c = Group.objects.get_or_create(pk=settings.ADMIN_GROUP_ID, name='admins')
        for row in cursor:
            (user_id, username, email, password, group_id, \
                last_login, date_joined) = row
            is_staff, is_active, is_superuser = 0, 1, 0
            if group_id == GROUP_ID_BANNED:
                is_active = 0
                group = banned_group
            if group_id == GROUP_ID_MOD:
                is_staff = 1
                group = mods_group
            if group_id == GROUP_ID_ADMIN:
                is_staff = 1
                is_superuser = 1
                group = admins_group
            if not last_login:
                import datetime
                last_login = datetime.datetime.now()
            u = User(pk=user_id, 
                username=username, 
                email=email, 
                password=password, 
                is_staff = is_staff, 
                is_active = is_active, 
                is_superuser = is_superuser, 
                last_login=last_login, 
                date_joined=date_joined, 
            )
            u.save()
            u.groups.add(group)
            u.save()

        transaction.commit()
        transaction.leave_transaction_management()

