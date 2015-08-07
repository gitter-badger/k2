from django.views.generic import create_update
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils.translation import ugettext
from django.contrib import messages

def get_current_user_form_class(form_class, user_id, user_field='user'):
    """ adds user_id to form_class """
    class custom_class(form_class):
        def __init__(self, data=None, *args, **kwargs):
            if data:
                # unnecessary if no data
                data = data.copy()
                data.update({user_field: user_id})
            return super(custom_class, self).__init__(data, *args, **kwargs)
    return custom_class

def create_object(request, model=None, template_name=None,
        template_loader=loader, extra_context=None, post_save_redirect=None,
        login_required=False, context_processors=None, form_class=None,
        current_user=False, pre_save_signal=None, post_save_signal=None,
        signal_kwarg_name='object'):
    '''
    Generic create_object view with extra functionality:
        current_user
            update __init__ of the form class to use current user as initial
        pre_save_signal
            signal to send before save
        post_save signal 
            signal to send after save
    '''
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = create_update.get_model_and_form_class(model, form_class)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save(commit=False)
            if current_user:
                new_object.user = request.user
            
            signal_kwargs = {
                'sender': new_object.__class__,
                signal_kwarg_name: new_object,
                'request': request
            }
            # Signal that the object is about to be saved
            if pre_save_signal:
                pre_save_signal.send(**signal_kwargs)
            new_object.save()
            form.save_m2m()
            
            # Signal that object was saved
            if post_save_signal:
                post_save_signal.send(**signal_kwargs)
            msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return create_update.redirect(post_save_redirect, new_object)
    else:
        form = form_class()

    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    }, context_processors)
    create_update.apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))

def update_object(request, current_user=False, *args, **kwargs):
    '''
    Generic create_object view with extra functionality:
        current_user
            update __init__ of the form class to use current user as initial
    '''
    if current_user:
        kwargs['slug_field'], kwargs['slug'] = 'user', request.user.id
        kwargs['form_class'] = get_current_user_form_class(kwargs['form_class'], request.user.id)
    return create_update.update_object(request, *args, **kwargs)
