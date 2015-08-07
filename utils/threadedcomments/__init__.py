from forms import AuthThreadedCommentForm

def get_form():
    return AuthThreadedCommentForm

def InstallThreadedComments():
    from django.contrib.contenttypes import generic
    from django.contrib.comments.views import comments
    from django.contrib.comments.managers import CommentManager

    import threadedcomments
    from threadedcomments import models
    from threadedcomments.templatetags.threadedcomments_tags import CommentListNode
    
    from k2.utils.voting.models import Vote

    from models import is_author, get_content_object_url, get_absolute_url
    from views.comments import post_comment
    from managers import all, get_extra_query_set, annotate_score, \
        get_content_type_id, annotate_num_votes_positive, \
        annotate_num_votes_negative, annotate_vote
    from templatetags.threadedcomments_tags import get_query_set

    # custom view
    comments.post_comment = post_comment
    # custom form
    threadedcomments.get_form = get_form
    # custom manager
    CommentManager.all = all
    CommentManager.get_extra_query_set = get_extra_query_set
    CommentManager.annotate_vote = annotate_vote
    CommentManager.annotate_score = annotate_score
    CommentManager.annotate_num_votes_positive = annotate_num_votes_positive
    CommentManager.annotate_num_votes_negative = annotate_num_votes_negative
    CommentManager.get_content_type_id = get_content_type_id
    # extra score field in get_comment_list templatetag
    CommentListNode.get_query_set = get_query_set
    # extra votes field
    models.ThreadedComment.is_author = is_author
    models.ThreadedComment.get_content_object_url = get_content_object_url
    models.ThreadedComment.get_absolute_url = get_absolute_url
    models.ThreadedComment.add_to_class('votes', generic.GenericRelation(Vote))
