from types import NoneType

from django.contrib.contenttypes.models import ContentType

from k2.utils.django.db.models import IfnullSum

def get_extra_query_set(self, with_user_vote=False, with_score=False, \
                    with_num_votes_positive=False, with_num_votes_negative=False):
    """
    Overwrites the get_query_set to return queryset with extra fields.
    """
    
    qs = self.get_query_set()
    if with_user_vote:
        qs = self.annotate_vote(qs, with_user_vote)
    if with_score:
        qs = self.annotate_score(qs)
    if with_num_votes_positive:
        qs = self.annotate_num_votes_positive(qs)
    if with_num_votes_negative:
        qs = self.annotate_num_votes_negative(qs)
    return qs
def all(self, **kwargs):
    return self.get_extra_query_set(**kwargs)
def get_content_type_id(self):
    return ContentType.objects.get_for_model(self.model).id
def annotate_vote(self, query_set, user_id):
    """Append vote field to the get_query_set"""
    if not isinstance(user_id, (int, long, NoneType)):
        raise TypeError('user_id parameter must be int or float, %s found' % type(user_id))
    if not user_id:
        # AnonymousUser
        return query_set.extra(select={'vote': 'NULL'})
    return query_set.extra(
        select={
            'vote': 'SELECT vote FROM votes ' \
                'WHERE (votes.object_id = django_comments.id AND votes.content_type_id = %s ' \
                'AND votes.user_id = %s )' % (self.get_content_type_id(), user_id),
        }
    )
def annotate_score(self, query_set):
    """Append num_votes field to the get_query_set"""
    return query_set.annotate(score=IfnullSum('votes__vote'))
def annotate_num_votes_positive(self, query_set):
    """Append num_votes_positive field to the get_query_set"""
    return query_set.extra(
        select={
            'num_votes_positive': 'SELECT COUNT(*) FROM votes ' \
                'WHERE (votes.object_id = django_comments.id AND votes.content_type_id = %s ' \
                'AND votes.vote > 0 )' % self.get_content_type_id(),
        }
    )
def annotate_num_votes_negative(self, query_set):
    """Append num_votes_negative field to the get_query_set"""
    return query_set.extra(
        select={
            'num_votes_negative': 'SELECT COUNT(*) FROM votes ' \
                'WHERE (votes.object_id = django_comments.id AND votes.content_type_id = %s ' \
                'AND votes.vote < 0 )' % self.get_content_type_id(),
        }
    )
