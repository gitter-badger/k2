from django.conf.urls.defaults import *

from k2.utils.django.views.generic.create_update import update_object
from k2.utils.django.core.urlresolvers import reverse_lazy

from k2.styles.forms import PartialUserStyleForm

userstyle_update_info = {
    'form_class': PartialUserStyleForm,
    'login_required': True,
    'post_save_redirect': reverse_lazy('styles:update_userstyle'),
    'template_name': 'styles/userstyle_form.html',
    'current_user': True,
}

urlpatterns = patterns('styles.views',
    url(r'^ustawienia/style/$', update_object, userstyle_update_info, name='update_userstyle'),
)