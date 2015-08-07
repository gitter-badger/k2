from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService, RegistrationFormNoFreeEmail

class RegistrationFormUniqueNoFreeEmailTOS(RegistrationFormUniqueEmail, RegistrationFormTermsOfService, RegistrationFormNoFreeEmail):
    bad_domains = ['mailinator.com', ]
