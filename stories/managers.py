from types import NoneType

from django.db import models
from django.db.models import Count, Sum, Q
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType

from generic_aggregation import generic_annotate

class CategoryManager(models.Manager):
    """
    Custom manager for the Category model.
    """
    def get_tree(self, root=None):
    	"""
    	Returns flat tree for root category
    	"""
        __category_dict = {}
        __category_root_list = []
        __category_children_dict = {}
        def add(category, root_id):
            __category_dict[category.id] = category
     	    if category.parent_id != root_id:
        	    __category_children_dict.setdefault(category.parent_id, []).append(category.id)
    	    else:
                __category_root_list.append(category.id)
        # check root
        if root:
            if isinstance(root, int):
                root_id = root
            else:
                root_id = root.id
        else:
            root_id = None
        # get list
    	children = list(self.get_query_set())
    	# index
    	for category in children:
    		add(category, root_id)
    	# return indexed
        root_cats = [__category_dict[key] for key in __category_root_list]
        return [{'object': c, 'children': [__category_dict[ckey] for ckey in __category_children_dict.setdefault(c.id, [])] } for c in root_cats ]


class TopCategoryManager(CategoryManager):
    """
    Custom manager for the Category model to return to categories
    """
    def get_query_set(self):
        """
        Overwrites the get_query_set to only return Categories without parents 
        in the queue.
        """
        return super(TopCategoryManager, self).get_query_set().filter(parent=None)

class StoryManager(models.Manager):
    """
    Custom manager for the Story model.
    """
    def get_extra_query_set(self, with_num_votes=False, with_num_votes_positive=False, \
                            with_num_votes_negative=False, with_num_comments=False, \
                            with_karma_positive=False, with_karma_negative=False, \
                            with_num_references=False, with_user_vote=False, \
                            with_user_watch=False, with_user_save=False, with_karma=False):
        """
        Overwrites the get_query_set to return queryset with extra fields.
        """
        
        qs = self.get_query_set()
        if with_user_vote:
            qs = self.annotate_vote(qs, with_user_vote)
        if with_num_votes:
            qs = self.annotate_num_votes(qs)
        if with_num_votes_positive:
            qs = self.annotate_num_votes_positive(qs)
        if with_num_votes_negative:
            qs = self.annotate_num_votes_negative(qs)
        if with_karma:
            qs = self.annotate_karma(qs)
        if with_karma_positive:
            qs = self.annotate_karma_positive(qs)
        if with_karma_negative:
            qs = self.annotate_karma_negative(qs)
        if with_num_comments:
            qs = self.annotate_num_comments(qs)
        if with_num_references:
            qs = self.annotate_num_references(qs)
        if with_user_watch:
            qs = self.annotate_watched(qs, with_user_watch)
        if with_user_save:
            qs = self.annotate_saved(qs, with_user_save)
        return qs
    def all(self, **kwargs):
        return self.get_extra_query_set(**kwargs)
    def get_popular(self, **kwargs):
        """
        Returns the get_query_set with popular Stories.
        """
        return self.get_extra_query_set(**kwargs).exclude(published_date=None)
    def get_upcoming(self, **kwargs):
        """
        Returns the get_query_set with upcoming Stories.
        """
        return self.get_extra_query_set(**kwargs).filter(published_date=None)
    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self.model).id
    def annotate_user(self, query_set, user_id):
        user_func = ['annotate_vote', 'annotate_saved', 'annotate_watched']
        for func in user_func:
            query_set = getattr(self, func)(query_set, user_id)
        return query_set
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
                    'WHERE (votes.object_id = stories_story.id AND votes.content_type_id = %s ' \
                    'AND votes.user_id = %s )' % (self.get_content_type_id(), user_id),
            }
        )
    def annotate_num_votes(self, query_set):
        """Append num_votes field to the get_query_set"""
        return query_set.annotate(num_votes=Count('votes'))
    def annotate_num_votes_positive(self, query_set):
        """Append num_votes_positive field to the get_query_set"""
        return query_set.extra(
            select={
                'num_votes_positive': 'SELECT COUNT(*) FROM votes ' \
                    'WHERE (votes.object_id = stories_story.id AND votes.content_type_id = %s ' \
                    'AND votes.vote > 0 )' % self.get_content_type_id(),
            }
        )
    def annotate_num_votes_negative(self, query_set):
        """Append num_votes_negative field to the get_query_set"""
        return query_set.extra(
            select={
                'num_votes_negative': 'SELECT COUNT(*) FROM votes ' \
                    'WHERE (votes.object_id = stories_story.id AND votes.content_type_id = %s ' \
                    'AND votes.vote < 0 )' % self.get_content_type_id(),
            }
        )
    def annotate_karma(self, query_set):
        """Append karma field to the get_query_set"""
        return query_set.extra(
            select={
                'karma': 'SELECT IFNULL(SUM(vote), 0) FROM votes ' \
                    'WHERE (votes.object_id = stories_story.id AND votes.content_type_id = %s )' \
                    % self.get_content_type_id(),
            }
        )
    def annotate_karma_positive(self, query_set):
        """Append karma_positive field to the get_query_set"""
        return query_set.extra(
            select={
                'karma_positive': 'SELECT IFNULL(SUM(vote), 0) FROM votes ' \
                    'WHERE (votes.object_id = stories_story.id AND votes.content_type_id = %s ' \
                    'AND votes.vote > 0 )' % self.get_content_type_id(),
            }
        )
    def annotate_karma_negative(self, query_set):
        """Append karma_negative field to the get_query_set"""
        return query_set.extra(
            select={
                'karma_negative': 'SELECT IFNULL(SUM(vote), 0) FROM votes ' \
                    'WHERE (votes.object_id = stories_story.id AND votes.content_type_id = %s ' \
                    'AND votes.vote < 0 )' % self.get_content_type_id(),
            }
        )
    def annotate_num_comments(self, query_set):
        """Append num_comments field to the get_query_set"""
        #@todo: is_removed based on COMMENTS_HIDE_REMOVED
        return query_set.extra(
            select={
                'num_comments': 'SELECT COUNT(*) FROM django_comments ' \
                    'WHERE (django_comments.site_id = 1 AND django_comments.object_pk = stories_story.id ' \
                    'AND django_comments.content_type_id = %s AND django_comments.is_public = True ' \
                    'AND django_comments.is_removed = False )' % self.get_content_type_id(),
            }
        )
        #return generic_annotate(query_set, Comment.content_object, Count('id'), alias='num_comments')
    def annotate_num_references(self, query_set):
        """Append num_references field to the get_query_set"""
        return query_set.annotate(num_references=Count('references'))
    def annotate_watched(self, query_set, user_id):
        """Append is_watched field to the get_query_set"""
        if not isinstance(user_id, (int, long, NoneType)):
            raise TypeError('user_id parameter must be int or float, %s found' % type(user_id))
        if not user_id:
            # AnonymousUser
            return query_set.extra(select={'is_watched': 'NULL'})
        return query_set.extra(
            select={
                'is_watched': 'SELECT CASE WHEN COUNT(1) > 0 THEN TRUE ELSE FALSE END FROM stories_watch ' \
                    'WHERE (stories_watch.story_id = stories_story.id ' \
                    'AND stories_watch.user_id = %s )' % user_id
            }
        )
    def annotate_saved(self, query_set, user_id):
        """Append is_saved field to the get_query_set"""
        if not isinstance(user_id, (int, long, NoneType)):
            raise TypeError('user_id parameter must be int or float, %s found' % type(user_id))
        if not user_id:
            # AnonymousUser
            return query_set.extra(select={'is_saved': 'NULL'})
        return query_set.extra(
            select={
                'is_saved': 'SELECT CASE WHEN COUNT(1) > 0 THEN TRUE ELSE FALSE END FROM stories_save ' \
                    'WHERE (stories_save.story_id = stories_story.id ' \
                    'AND stories_save.user_id = %s )' % user_id,
            }
        )
    def search(self, query_set, query):
        """Search filter for the query_set"""
        search_filter = (
            Q(title__icontains=query) |
            Q(url__icontains=query) |
            Q(summary__icontains=query)
        )
        return query_set.filter(search_filter)

class OpenStoryManager(StoryManager):
    """
    Extra manager for the Story model.
    """
    def get_query_set(self):
        """
        Overwrites the get_query_set to only return open Stories.
        """
        return super(OpenStoryManager, self).get_query_set().filter(is_public=True, is_removed=False, is_locked=False)

class AccessibleStoryManager(StoryManager):
    """
    Extra manager for the Story model.
    """
    def get_query_set(self):
        """
        Overwrites the get_query_set to only return accessible Stories.
        """
        return super(AccessibleStoryManager, self).get_query_set().filter(is_removed=False)
