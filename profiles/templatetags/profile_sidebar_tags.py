from django import template

from invitation.models import InvitationKey

from k2.utils.invitation.forms import InvitationKeyForm

register = template.Library()

remaining_invitations_for_user = InvitationKey.objects.remaining_invitations_for_user

@register.inclusion_tag('profiles/templatetags/sidebar_invite.html', takes_context=True)
def sidebar_invite(context):
    request = context['request']
    site = context['site']
    if not request.user.is_authenticated():
        return {'site': site}
    remaining_invitations = remaining_invitations_for_user(request.user)
    form = InvitationKeyForm()
    return {'site': site, 'form': form, 'remaining_invitations': remaining_invitations}