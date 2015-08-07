from django.conf import settings
from django.utils.encoding import smart_unicode

def get_query_set(self, context):
    request = context['request']
    ctype, object_pk = self.get_target_ctype_pk(context)
    if not object_pk:
        return self.comment_model.objects.none()

    qs = self.comment_model.objects.all(with_user_vote=request.user.id, with_score=True, \
                        with_num_votes_positive=True, with_num_votes_negative=True).filter(
        content_type = ctype,
        object_pk    = smart_unicode(object_pk),
        site__pk     = settings.SITE_ID,
    ).select_related('user', 'user__profile')
    if not request.user.has_perms('comments.can_moderate'):
        qs = qs.filter(is_public=True)
    if getattr(settings, 'COMMENTS_HIDE_REMOVED', True):
        qs = qs.filter(is_removed=False)
    return qs