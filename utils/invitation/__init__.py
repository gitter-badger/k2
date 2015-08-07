def InstallInvtation():
    from django.contrib.auth.models import User
    
    from invitation.models import InvitationUser, InvitationKey, InvitationKeyManager
    
    from managers import used
    from models import inviter, last_update, registrant
    
    # inviter field replace
    InvitationUser._meta.local_fields[1] = inviter
    InvitationUser._meta.local_fields[1].set_attributes_from_name('inviter')
    InvitationUser._meta.local_fields[1].model = InvitationUser
    # registrant field relation remove
    delattr(User, 'invitations_used')
    # registrant field replace
    InvitationKey._meta.local_fields[4] = registrant
    InvitationKey._meta.local_fields[4].set_attributes_from_name('registrant')
    InvitationKey._meta.local_fields[4].model = InvitationKey
    # registrant field new relation
    InvitationKey._meta.local_fields[4].contribute_to_class(InvitationKey, 'registrant')
    InvitationKey._meta.local_fields.pop(4)
    # extra fields
    InvitationUser.add_to_class('last_update', last_update)
    
    # extra method for manager
    setattr(InvitationKeyManager, 'used', used)
