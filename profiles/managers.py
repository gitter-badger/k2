from django.db import models

class ProfileManager(models.Manager):
    """
    Custom manager for the UserProfile model.
    """
    def get_extra_query_set(self, with_num_comments=False, with_num_published=False, \
                            with_num_stories=False):
        """
        Overwrites the get_query_set to return queryset with extra fields.
        """
        
        qs = super(ProfileManager, self).get_query_set()
        if with_num_comments:
            qs = self.annotate_num_comments(qs)
        if with_num_published:
            qs = self.annotate_num_published(qs)
        if with_num_stories:
            qs = self.annotate_num_stories(qs)
        return qs
    def all(self, **kwargs):
        return self.get_extra_query_set(**kwargs)
    def annotate_num_comments(self, query_set):
        """Append num_comments field to the get_query_set"""
        #@todo: is_removed based on COMMENTS_HIDE_REMOVED
        return query_set.extra(
            select={
                'num_comments': 'SELECT COUNT(*) FROM django_comments ' \
                    'WHERE django_comments.user_id = profiles_userprofile.user_id ' \
                    'AND is_public = True AND is_removed = False',
            }
        )
    def annotate_num_published(self, query_set):
        """Append num_published field to the get_query_set"""
        return query_set.extra(
            select={
                'num_published': 'SELECT COUNT(*) FROM stories_story ' \
                    'WHERE stories_story.published_date IS NOT NULL AND stories_story.user_id = profiles_userprofile.user_id ' \
                    'AND stories_story.is_public = 1',
            }
        )
    def annotate_num_stories(self, query_set):
        """Append num_stories field to the get_query_set"""
        return query_set.extra(
            select={
                'num_stories': 'SELECT COUNT(*) FROM stories_story ' \
                    'WHERE stories_story.user_id = profiles_userprofile.user_id ' \
                    'AND stories_story.is_public = 1',
            }
        )
