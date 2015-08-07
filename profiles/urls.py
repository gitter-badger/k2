from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.views import login, logout, password_change, \
    password_reset_confirm, password_reset_complete
from django.contrib.auth.decorators import login_required
from django.contrib import comments

from invitation.views import invite, invited, register
from registration.views import activate
from invitation.models import InvitationKey

from k2.utils.voting.models import Vote
from k2.utils.django.views.generic.create_update import update_object
from k2.utils.django.views.generic.list_detail import object_detail_list
from k2.utils.django.core.urlresolvers import reverse_lazy
from k2.utils.django.contrib.auth.decorators import anonymous_required
from k2.utils.registration.forms import RegistrationFormUniqueNoFreeEmailTOS

from k2.profiles.forms import PartialProfileForm, AvatarForm
from k2.profiles.models import UserProfile
from k2.profiles.views import change_password_done
from k2.stories.models import Story

profile_list_info = {
    'paginate_by': 10,
    'queryset': UserProfile.objects.all(with_num_comments=True, with_num_published=True, with_num_stories=True) \
            .select_related(),
    'template_object_name': 'profile',
    'template_name': 'profiles/profile_list.html',
}

profile_detail_info = {
    'paginate_by': 10,
    'queryset': UserProfile.objects.all().select_related(),
    'template_object_name': 'profile',
    'slug_field': 'user__username',
}

profile_digs_info = {
    'template_name': 'profiles/profile_detail_diggs.html',
    'related_field': 'votes__user__profile',
    'list_queryset': Story.open.all(with_num_votes_positive=True) \
            .select_related().order_by('-created_date').filter(votes__vote__gt=0),
    'template_object_list_name': 'story',
}

profile_stories_info = {
    'template_name': 'profiles/profile_detail_stories.html',
    'related_field': 'user__profile',
    'list_queryset': Story.open.all(with_num_votes_positive=True) \
            .select_related().order_by('-created_date'),
    'template_object_list_name': 'story',
}

profile_comments_info = {
    'template_name': 'profiles/profile_detail_comments.html',
    'related_field': 'user__profile',
    'list_queryset': comments.get_model().objects.all(with_score=True, \
            with_num_votes_positive=True, with_num_votes_negative=True) \
            .select_related('user', 'user__profile').order_by('-submit_date'),
    'template_object_list_name': 'comment',
}

profile_invites_info = {
    'paginate_by': None,
    'template_name': 'profiles/profile_detail_invites.html',
    'related_field': 'from_user__profile',
    'list_queryset': InvitationKey.objects.exclude(registrant=None).select_related().order_by('-date_invited'),
    'template_object_list_name': 'invite',
}

profile_update_info = {
    'form_class': PartialProfileForm,
    'login_required': True,
    'post_save_redirect': reverse_lazy('profiles:update_profile'),
    'template_name': 'profiles/profile_form.html',
    'current_user': True,
}

avatar_update_info = {
    'form_class': AvatarForm,
    'login_required': True,
    'post_save_redirect': reverse_lazy('profiles:update_avatar'),
    'template_name': 'profiles/avatar_form.html',
    'current_user': True,
}

password_change_info = {
    'template_name': 'profiles/password_change_form.html',
    'post_change_redirect': reverse_lazy('profiles:change_password_done'),
}

password_change_done_info = {
    'template_name': 'profiles/password_change_form.html',
    'post_change_redirect': '/ustawienia/haslo/',
}

invite_info = {
    'success_url': reverse_lazy('profiles:invitation_complete'),
    'template_name': 'invitation/invitation_form.html',
}

invitation_complete_info = {
    'template': 'invitation/invitation_complete.html',
}

register_info = {
    'backend': 'registration.backends.default.DefaultBackend',
    'form_class': RegistrationFormUniqueNoFreeEmailTOS,
    'success_url': reverse_lazy('profiles:registration_complete'),
}

invitation_register_info = {
    'backend': 'profiles.backends.InvitationBackend',
    'success_url': None,
}

registration_complete_info = {
    'template': 'registration/registration_complete.html',
}

activate_info = {
    'backend': 'registration.backends.default.DefaultBackend',
    'success_url': reverse_lazy('profiles:registration_activation_complete'),
}

activation_complete_info = {
    'template': 'registration/activate.html',
    'extra_context': {'account': True},
}

if getattr(settings, 'INVITE_MODE', False):
    register_info.update(invitation_register_info)

urlpatterns = patterns('profiles.views',
    url(r'^ranking/$', object_list, profile_list_info, name='profile_list'), 
    url(r'^profil/(?P<page>\d+|last)/$', object_list, profile_list_info, name='profile_list'),
    url(r'^logowanie/$', anonymous_required(login), {'template_name': 'profiles/login.html'}, name="login"),
    url(r'^wyloguj/$', logout, name="logout"),
    # settings
    url(r'^ustawienia/haslo/$', password_change, password_change_info, name="password_change"),
    url(r'^ustawienia/haslo/ok/$', change_password_done, password_change_done_info, name="change_password_done"),
    url(r'^ustawienia/profil/$', update_object, profile_update_info, name='update_profile'),
    url(r'^ustawienia/avatar/$', update_object, avatar_update_info, name='update_avatar'),
    # profile views
    url(r'^profil/(?P<slug>[0-9a-zA-Z_-]+)/$', login_required(object_detail_list), dict(profile_digs_info, **profile_detail_info), name='profile'),
    url(r'^profil/(?P<slug>[0-9a-zA-Z_-]+)/dodane/$', login_required(object_detail_list), dict(profile_stories_info, **profile_detail_info), name='profile_stories'),
    url(r'^profil/(?P<slug>[0-9a-zA-Z_-]+)/komentowane/$', login_required(object_detail_list), dict(profile_comments_info, **profile_detail_info), name='profile_comments'),
    url(r'^profil/(?P<slug>[0-9a-zA-Z_-]+)/zaproszeni/$', login_required(object_detail_list), dict(profile_invites_info, **profile_detail_info), name='profile_invites'),
    # invitation, activation & registration
    url(r'^rejestracja/$', register, register_info, 'registration_register'),
    url(r'^rejestracja/ok/$', direct_to_template, registration_complete_info, 'registration_complete'),
    url(r'^aktywacja/ok/$', direct_to_template, activation_complete_info, 'registration_activation_complete'),
    url(r'^aktywacja/(?P<activation_key>\w+)/$', activate, activate_info, 'registration_activate'),
    url(r'^zapros/$', invite, invite_info, 'invitation_invite'),
    url(r'^zapros/ok/$', direct_to_template, invitation_complete_info, 'invitation_complete'),
    #url(r'^zaproszenie/(?P<invitation_key>\w+)/$', invited, name='invitation_invited'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='auth_password_reset_confim',),
    url(r'^reset/ok/$', password_reset_complete),
)
