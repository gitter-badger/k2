from django.contrib import admin
from django.contrib.comments.models import Comment
from django.contrib.comments.admin import CommentsAdmin

from k2.stories.models import Category, Story, Reference, Watch, Save, UserPref
from k2.stories.forms import StoryAdminForm

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', '__unicode__', )
    list_display_links = ('__unicode__', )
    search_fields = ['__unicode__', ]
    inlines = [CategoryInline]
    prepopulated_fields = {'slug': ('name',)}

    def queryset(self, request):
        return Category.top_categories.filter(parent=None)

class StoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'url', )
    list_filter = ('is_public', 'is_removed', 'is_locked')
    prepopulated_fields = {'slug': ('title',)}
    form = StoryAdminForm
    inlines = [ReferenceInline]

admin.site.register(Comment, CommentsAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Reference)
admin.site.register(Save)
admin.site.register(Watch)
admin.site.register(UserPref)

