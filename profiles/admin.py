from django.contrib import admin

from k2.profiles.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['user']}),
        ('User information',    {'fields': ['about', 'location', 'gender', 'gg', 'jabber', 'website', 'email_show']}),
        ('Avatar',              {'classes': ('collapse',), 'fields': ['avatar']}),
        ('User ranking',        {'classes': ('collapse',), 'fields': ['userclass']}),
    ]

admin.site.register(UserProfile, UserProfileAdmin)

