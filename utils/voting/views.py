from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.create_update import redirect
from django.utils import simplejson

from forms import ObjectVoteForm
from models import Vote
import signals

def vote_on_object(request, model, karma, post_save_redirect=None,
        object_id=None, slug=None, slug_field=None, allow_xmlhttprequest=False):
    """
    Enchanced generic object vote function.

    Messages are used to confirm the vote; vote registration 
    will only be performed if this view is POSTed.

    If ``allow_xmlhttprequest`` is ``True`` and an XMLHttpRequest is
    detected by examining the ``HTTP_X_REQUESTED_WITH`` header, the
    ``xmlhttp_vote_on_object`` view will be used to process the
    request - this makes it trivial to implement voting via
    XMLHttpRequest with a fallback for users who don't have JavaScript
    enabled.
    """
    if allow_xmlhttprequest and request.is_ajax():
        # @todo: replace with karma vote
        return xmlhttprequest_vote_on_object(request, model, 'up',
                                             object_id=object_id, slug=slug,
                                             slug_field=slug_field)

    # login always required
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)

    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError('Generic vote view must be called with either '
                             'object_id or slug and slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except model.DoesNotExist:
        raise Http404, 'No %s found for %s.' % (model._meta.app_label, lookup_kwargs)

    if request.method == "POST":
        ctype = ContentType.objects.get_for_model(model)
        initial = {'user': request.user.id, 'content_type': ctype.id, \
            'object_id': obj._get_pk_val(), 'vote': karma}
        vote = Vote.objects.get_for_user(obj, request.user)
        post = request.POST.copy()
        post.update(initial)
        if not vote:
            form = ObjectVoteForm(post)
        else:
            form = ObjectVoteForm(post, instance=vote)
        if form.is_valid():
            vote_object = form.save(commit=False)
            signals.vote_will_be_saved.send(sender=Vote, vote=vote_object, obj=obj, request=request)
            vote_object.save()
            form.save_m2m()
            signals.vote_was_saved.send(sender=Vote, vote=vote_object, obj=obj, request=request)
            if vote_object.vote == 0:
                messages.add_message(request, messages.SUCCESS, _('Undo vote successful'))
            else:
                messages.add_message(request, messages.SUCCESS, _('Voted successful'))
        else:
            messages.add_message(request, messages.ERROR, _('Vote form invalid') + unicode(form.errors))
    else:
        messages.add_message(request, messages.ERROR, _('Vote form not sent'))
    return redirect(post_save_redirect, obj)

def json_error_response(error_message):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))

def xmlhttprequest_vote_on_object(request, model, direction,
    object_id=None, slug=None, slug_field=None):
    """
    Generic object vote function for use via XMLHttpRequest.


    Properties of the resulting JSON object:
        success
            ``true`` if the vote was successfully processed, ``false``
            otherwise.
        score
            The object's updated score and number of votes if the vote
            was successfully processed.
        error_message
            Contains an error message if the vote was not successfully
            processed.
    """
    if request.method == 'GET':
        return json_error_response(
            'XMLHttpRequest votes can only be made using POST.')
    if not request.user.is_authenticated():
        return json_error_response('Not authenticated.')


    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        return json_error_response(
            '\'%s\' is not a valid vote type.' % direction)


    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        return json_error_response('Generic XMLHttpRequest vote view must be '
                                   'called with either object_id or slug and '
                                   'slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        return json_error_response(
            'No %s found for %s.' % (model._meta.verbose_name, lookup_kwargs))


    # Vote and respond
    Vote.objects.record_vote(obj, request.user, vote)
    return HttpResponse(simplejson.dumps({
        'success': True,
        'score': Vote.objects.get_score(obj),
    }))