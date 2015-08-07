from django.contrib import admin

from k2.styles.models import UserStyle
from k2.styles.forms import UserStyleForm

class UserStyleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'style', 'night_style', )

    form = UserStyleForm

admin.site.register(UserStyle, UserStyleAdmin)

