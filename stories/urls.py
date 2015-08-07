from datetime import datetime, timedelta

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from tagging.views import tagged_object_list

from k2.utils.django.views.generic.create_update import update_object
from k2.utils.django.core.urlresolvers import reverse_lazy
from k2.utils.voting.views import vote_on_object

from k2.stories.forms import PartialStoryForm, ReferenceForm, PartialUserPrefForm
from k2.stories.models import Category, Story
from k2.stories.views.stories import story_detail, story_list, category_list, \
    search_list, create_story, dig_story, bury_story, domain_object_list
from k2.stories.views.moderation import flag, delete, approve, lock
from k2.stories.views.references import create_reference_detail
from k2.stories.views.userlists import saved_list, watched_list, check_save, uncheck_save, check_watch, uncheck_watch
from k2.stories.feeds import PopularStoriesFeed, UpcomingStoriesFeed, LatestCommentsFeed, StoryCommentsFeed
from k2.stories import settings as stories_settings

detail_story_qs = Story.accessible.all(with_num_votes=True, \
            with_num_votes_positive=True, with_num_votes_negative=True, \
            with_num_comments=True, with_num_references=True).select_related()

list_story_qs = Story.open.all(with_num_votes=True, \
            with_num_votes_positive=True, with_num_votes_negative=True, \
            with_num_comments=True, with_num_references=True).select_related()

story_detail_info = {
    'queryset': detail_story_qs,
    'template_object_name': 'story',
}

story_search_info = {
    'queryset': list_story_qs.distinct().order_by('-num_votes'),
}

story_tagged_info = {
    'queryset_or_model': list_story_qs.distinct().order_by('-num_votes'),
}

story_references_info = {
    'template_name': 'stories/story_detail_references.html',
    'form_class': ReferenceForm,
    'login_required': True,
}

story_digs_info = {
    'template_name': 'stories/story_detail_digs.html',
}

story_buries_info = {
    'template_name': 'stories/story_detail_buries.html',
}

story_list_info = {
    'template_object_name': 'story',
    'paginate_by': 3,
}

story_create_update_info = {
    'form_class': PartialStoryForm,
    'login_required': True,
    'current_user': True,
}

story_create_info = {
    'template_name': 'stories/story_form_create.html',
}

story_update_info = {
    'current_user': False,
    'template_name': 'stories/story_form_update.html',
}

popular_list_info = {
    'list_type': 'popular',
    'queryset': list_story_qs.exclude(published_date=None),
    'template_name': 'stories/story_list_popular.html',
}

upcoming_list_info = {
    'list_type': 'upcoming',
    'queryset': list_story_qs.filter(published_date=None, created_date__gt=datetime.now()-timedelta(days=stories_settings.STORY_LIFE_TIME)),
    'template_name': 'stories/story_list_upcoming.html',
}

saved_list_info = {
    'list_type': 'saved',
    'queryset': list_story_qs.distinct(),
    'template_name': 'stories/story_list_saved.html',
}

watched_list_info = {
    'list_type': 'watched',
    'queryset': list_story_qs.distinct(),
    'template_name': 'stories/story_list_watched.html',
}

vote_on_story_info = {
    'model': Story,
}

dig_story_info = {
    'karma': 1,
}

undig_story_info = {
    'karma': 0,
}

bury_story_info = {
    'karma': -1,
}

userpref_update_info = {
    'form_class': PartialUserPrefForm,
    'login_required': True,
    'post_save_redirect': reverse_lazy('stories:update_userpref'),
    'template_name': 'stories/userpref_form.html',
    'current_user': True,
}

urlpatterns = patterns('stories.views',
    url(r'^$', story_list, dict(popular_list_info, **story_list_info), 'popular_story_list'), 
    #url(r'^(?P<page>\d+|last)/$', story_list, dict(popular_list_info, **story_list_info), 'popular_story_list'),
    url(r'^przedpokoj/$', login_required(story_list), dict(upcoming_list_info, **story_list_info), 'upcoming_story_list'), 
    #url(r'^przedpokoj/(?P<page>\d+|last)/$', login_required(story_list), dict(upcoming_list_info, **story_list_info), 'upcoming_story_list'), 
    url(r'^zapisane/$', login_required(saved_list), dict(saved_list_info, **story_list_info), 'saved_story_list'), 
    #url(r'^zapisane/(?P<page>\d+|last)/$', login_required(saved_list), dict(saved_list_info, **story_list_info), 'saved_story_list'), 
    url(r'^obserwowane/$', login_required(watched_list), dict(watched_list_info, **story_list_info), 'watched_story_list'), 
    #url(r'^obserwowane/(?P<page>\d+|last)/$', login_required(watched_list), dict(watched_list_info, **story_list_info), 'watched_story_list'), 
    url(r'^link/(?P<object_id>\d+)/$', story_detail, story_detail_info, 'story'), 
    url(r'^link/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', story_detail, story_detail_info, 'story_slug'), 
    url(r'^ramka/(?P<object_id>\d+)/$', story_detail, story_detail_info, 'frame'), 
    url(r'^ramka/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', story_detail, story_detail_info, 'frame_slug'), 
    url(r'^dodaj_link/$', login_required(create_story), dict(story_create_update_info, **story_create_info), 'story_add'), 
    url(r'^edytuj/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', login_required(update_object), dict(story_create_update_info, **story_update_info), 'story_edit'), 
    # filtered
    #  searched
    url(r'^szukaj/$', search_list, dict(story_search_info, **story_list_info), 'search'), 
    #  tagged
    url(r'^tag/(?P<tag>[-\w]+)/$', tagged_object_list, dict(story_tagged_info, **story_list_info), 'tagged'), 
    #  domain
    url(r'^domena/(?P<domain>([0-9a-z][-\w]*[0-9a-z]\.)+[a-z0-9\-]{2,15})/$', domain_object_list, dict(story_search_info, **story_list_info), 'domain'),
    # save
    url(r'^zapisane/dodaj/(?P<object_id>\d+)/$', login_required(check_save), {}, 'story_save'), 
    url(r'^zapisane/usun/(?P<object_id>\d+)/$', login_required(uncheck_save), {}, 'story_unsave'), 
    # watch
    url(r'^obserwowane/dodaj/(?P<object_id>\d+)/$', login_required(check_watch), {}, 'story_watch'), 
    url(r'^obserwowane/usun/(?P<object_id>\d+)/$', login_required(uncheck_watch), {}, 'story_unwatch'), 
    # voting
    url(r'^za/glosuj/(?P<object_id>\d+)/$', login_required(dig_story), dict(dig_story_info, **vote_on_story_info), 'dig_story'), 
    url(r'^za/glosuj/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', login_required(dig_story), dict(dig_story_info, **vote_on_story_info), 'dig_story_slug'),
    url(r'^za/cofnij/(?P<object_id>\d+)/$', login_required(vote_on_object), dict(undig_story_info, **vote_on_story_info), 'undig_story'), 
    url(r'^za/cofnij/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', login_required(vote_on_object), dict(undig_story_info, **vote_on_story_info), 'undig_story_slug'),
    url(r'^przeciw/glosuj/(?P<object_id>\d+)/$', login_required(bury_story), dict(bury_story_info, **vote_on_story_info), 'bury_story'), 
    url(r'^przeciw/glosuj/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', login_required(bury_story), dict(bury_story_info, **vote_on_story_info), 'bury_story_slug'),
    # settings
    url(r'^ustawienia/$', update_object, userpref_update_info, 'update_userpref'),
    # references
    url(r'^powiazane/(?P<object_id>\d+)/$', create_reference_detail, dict(story_references_info, **story_detail_info), 'references'), 
    url(r'^powiazane/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', create_reference_detail, dict(story_references_info, **story_detail_info), 'references_slug'), 
    # digs
    url(r'^za/(?P<object_id>\d+)/$', story_detail, dict(story_digs_info, **story_detail_info), 'digs'), 
    url(r'^za/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', story_detail, dict(story_digs_info, **story_detail_info), 'digs_slug'), 
    # buries
    url(r'^przeciw/(?P<object_id>\d+)/$', story_detail, dict(story_buries_info, **story_detail_info), 'buries'), 
    url(r'^przeciw/(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', story_detail, dict(story_buries_info, **story_detail_info), 'buries_slug'), 
    # moderation
    url(r'^oflaguj/(\d+)/$', flag, name='story_flag'),
    url(r'^usun/(\d+)/$',  delete, name='story_delete'),
    url(r'^zatwierdz/(\d+)/$', approve, name='story_approve'),
    url(r'^zablokuj/(\d+)/$', lock, name='story_lock'),
    # categories (must be last)
    url(r'^(?P<slug>[-\w]+)/$', category_list, dict(popular_list_info, **story_list_info), 'popular_category_list'), 
    url(r'^(?P<slug>[-\w]+)/przedpokoj/$', login_required(category_list), dict(upcoming_list_info, **story_list_info), 'upcoming_category_list'), 
    # feeds
    url(r'^rss/popularne/$', PopularStoriesFeed(), name='popular_feed'),
    url(r'^rss/najnowsze/$', UpcomingStoriesFeed(), name='upcoming_feed'),
    url(r'^rss/komentarze/$', LatestCommentsFeed(), name='comment_feed'),
    url(r'^rss/komentarze/(?P<object_id>\d+)/$', StoryCommentsFeed(), name='story_feed'),
)
