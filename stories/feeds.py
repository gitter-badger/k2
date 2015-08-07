from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from k2.stories.models import Story

current_site = Site.objects.get_current()

class StoriesFeed(Feed):
    title = _("%(site_name)s stories") % dict(site_name=Site.objects.get_current())

    def item_title(self, obj):
        return obj.title

    def item_description(self, obj):
        return obj.summary

    def item_author_name(self, obj):
        return obj.user.username

    def item_author_link(self, obj):
        return obj.user.get_profile().url

    def item_categories(self, obj):
        return [obj.category,]

class PopularStoriesFeed(StoriesFeed):
    link = "/"
    description = _("Popular stories")

    def items(self):
        return Story.open.get_popular().order_by('-published_date')[:5]

class UpcomingStoriesFeed(StoriesFeed):
    link = "/przedpokoj/"
    description = _("Newest stories")

    def items(self):
        return Story.open.get_upcoming().order_by('-created_date')[:5]

class LatestCommentsFeed(LatestCommentFeed):
    def items(self):
        return super(LatestCommentsFeed, self).items()[:5]

class StoryCommentsFeed(LatestCommentFeed):
    def get_object(self, request, object_id):
        return Story.objects.get(pk=object_id)

    def description(self, obj):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("Latest comments on %(site_name)s for %(story_title)s") % dict(site_name=self._site.name, story_title=obj.title)

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return Comment.objects.for_model(obj).filter(is_public=True, is_removed=False).order_by('-submit_date')[:5]
