from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.comments.views',
    url(r'^dodaj/$',          'comments.post_comment',       name='comments-post-comment'),
    url(r'^dodany/$',        'comments.comment_done',       name='comments-comment-done'),
    #url(r'^oflaguj/(\d+)/$',    'moderation.flag',             name='comments-flag'),
    #url(r'^oflagowany/$',       'moderation.flag_done',        name='comments-flag-done'),
    #url(r'^usun/(\d+)/$',  'moderation.delete',           name='comments-delete'),
    #url(r'^usuniety/$',       'moderation.delete_done',      name='comments-delete-done'),
    #url(r'^zatwierdz/(\d+)/$', 'moderation.approve',          name='comments-approve'),
    #url(r'^zatwierdzony/$',      'moderation.approve_done',     name='comments-approve-done'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)

urlpatterns += patterns('k2.utils.threadedcomments.views',
    url(r'^edytuj/(\d+)/$',          'comments.edit',       name='comments-edit'),
    url(r'^wyedytowany/$',        'comments.edit_done',       name='comments-edit-done'),
    url(r'^oflaguj/(\d+)/$',    'moderation.flag',             name='comments-flag'),
    url(r'^usun/(\d+)/$',  'moderation.delete',           name='comments-delete'),
    url(r'^zatwierdz/(\d+)/$', 'moderation.approve',          name='comments-approve'),
)