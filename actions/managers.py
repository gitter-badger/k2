from django.db import models
from django.contrib.contenttypes.models import ContentType

from k2.stories.models import Story

story_ctype = ContentType.objects.get_for_model(Story).id

class ActionManager(models.Manager):
    """
    Custom manager for the Action model.
    """
    def get_query_set(self):
        """
        Overwrites the get_query_set to return combined data.
        """
        return self.raw("""
            SELECT t.*
            FROM (
                SELECT date_modified AS date_added, object_id AS story_id, user_id, 1 AS type 
                FROM votes
                WHERE vote < 0 AND content_type_id = %(content_type_id)s
                UNION
                SELECT date_modified AS date_added, object_id AS story_id, user_id, 2 AS type 
                FROM votes
                WHERE vote > 0 AND content_type_id = %(content_type_id)s
                UNION
                SELECT submit_date AS date_added, object_pk AS story_id, user_id, 3 AS type 
                FROM django_comments
                WHERE is_public = True AND is_removed = False
                UNION
                SELECT created_date AS date_added, id AS story_id, user_id, 4 AS type 
                FROM stories_story
                WHERE published_date IS NULL AND is_public = True AND is_removed = False
                UNION
                SELECT published_date AS date_added, id AS story_id, user_id, 5 AS type 
                FROM stories_story
                WHERE published_date IS NOT NULL AND is_public = True AND is_removed = False
                UNION
                SELECT created_date AS date_added, story_id, user_id, 6 AS type 
                FROM stories_reference
                WHERE is_public = True AND is_removed = False
            ) AS t
            ORDER BY t.date_added DESC
        """ % {"content_type_id": story_ctype})
