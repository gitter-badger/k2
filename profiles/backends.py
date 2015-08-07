from invitation import backends

class InvitationBackend(backends.InvitationBackend):
    def post_registration_redirect(self, request, user, *args, **kwargs):
        super(InvitationBackend, self).post_registration_redirect(request, user, *args, **kwargs)
        return ('profiles:registration_complete', (), {})