from django.db import models
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers

def dfs(node, all_nodes, depth):
    """
    Performs a recursive depth-first search starting at ``node``.  This function
    also annotates an attribute, ``depth``, which is an integer that represents
    how deeply nested this node is away from the original object.
    """
    node.depth = depth
    to_return = [node,]
    for subnode in all_nodes:
        if subnode.parent_id == node.id:
        #if subnode.parent and subnode.parent.id == node.id:
            to_return.extend(dfs(subnode, all_nodes, depth+1))
    return to_return

def get_tree(self, content_object, root=None):
    """
    Runs a depth-first search on all comments related to the given content_object.
    This depth-first search adds a ``depth`` attribute to the comment which
    signifies how how deeply nested the comment is away from the original object.
    
    If root is specified, it will start the tree from that comment's ID.
    
    Ideally, one would use this ``depth`` attribute in the display of the comment to
    offset that comment by some specified length.
    
    The following is a (VERY) simple example of how the depth property might be used in a template:
    
        {% for comment in comment_tree %}
            <p style="margin-left: {{ comment.depth }}em">{{ comment.comment }}</p>
        {% endfor %}
    """
    content_type = ContentType.objects.get_for_model(content_object)
    children = list(self.get_query_set().filter(
        content_type = content_type,
        object_id = getattr(content_object, 'pk', getattr(content_object, 'id')),
    ).select_related('user__profile', 'votes').order_by('date_submitted'))
    to_return = []
    if root:
        if isinstance(root, int):
            root_id = root
        else:
            root_id = root.id
        to_return = [c for c in children if c.id == root_id]
        if to_return:
            to_return[0].depth = 0
            for child in children:
                if child.parent_id == root_id:
                    to_return.extend(dfs(child, children, 1))
    else:
        for child in children:
            if not child.parent_id:
            #if not child.parent:
                to_return.extend(dfs(child, children, 0))
    return to_return

def get_content_object_url(self):
    """
    Get a URL suitable for redirecting to the content object.
    """
    # Look up the object, making sure it's got a get_absolute_url() function.
    try:
        content_type = ContentType.objects.get(pk=self.content_type_id)
        if not content_type.model_class():
            raise Http404("Content type %s object has no associated model" % self.content_type_id)
        obj = content_type.get_object_for_this_type(pk=self.object_pk)
    except (ObjectDoesNotExist, ValueError):
        raise Http404("Content type %s object %s doesn't exist" % (self.content_type_id, self.object_pk))
    try:
        return obj.get_absolute_url()
    except AttributeError:
        raise Http404("%s objects don't have get_absolute_url() methods" % content_type.name)

def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
    return self.get_content_object_url() + (anchor_pattern % self.__dict__)

def is_author(self, user):
    return self.user == user
