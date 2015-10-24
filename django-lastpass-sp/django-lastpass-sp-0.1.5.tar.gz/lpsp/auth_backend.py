from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User


class SAMLServiceProviderBackend(object):

    def authenticate(self, saml_authentication=None):
        '''
        Username selection goes as follows:

        The default username for user@domain.tld is user. If the email for
        the user does not match, another user with the same email is assumed.

        To use a custom format for usernames, define them as a format string
        in LASTPASS_USERNAME_FORMAT. The result needs to be unique so use
        either "user", "domain" or "email" in your format string. Examples:

            # example-bob for bob@example.com
            LASTPASS_USERNAME_FORMAT = '{domain}-{user}'

            # alice-alice@example.com for alice@example.com (silly)
            LASTPASS_USERNAME_FORMAT = '{user}-{email}'

            # carol+filter@example.com
            LASTPASS_USERNAME_FORMAT = '{user}+filter@{domain}'

        If there are many users with the same email, it is assumed that the
        username is the email. The full email as username can be made the
        default by setting LASTPASS_FULL_EMAIL_USERNAME = True in Django
        settings.

        If there is no user matching the email by name or email, the attempt
        is given up and a new user gets created.

        A new user is created either with the name part of the email or if
        there is a user with that name, the email address is used.

        This makes sure that the LastPass users always get the best match for
        username.

        All users authenticated through LastPass will be made active.
        '''
        if not saml_authentication:  # Using another authentication method
            return None

        if saml_authentication.is_authenticated():
            superuser = getattr(settings, 'LASTPASS_CREATE_ADMIN', False)
            staff = getattr(settings, 'LASTPASS_CREATE_STAFF', False)

            email = saml_authentication.get_nameid()
            preferred_name, domain = email.split('@', 1)

            username_format = getattr(settings, 'LASTPASS_USERNAME_FORMAT', None)

            if username_format:
                preferred_name = username_format.format(email=email,
                                                        user=preferred_name,
                                                        domain=domain)
            elif getattr(settings, 'LASTPASS_USERNAME_FULL_EMAIL', False):
                preferred_name = email

            try:
                try:
                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={'username': preferred_name,
                                  'is_superuser': superuser,
                                  'is_staff': staff}
                    )
                except User.MultipleObjectsReturned:
                    user, created = User.objects.get_or_create(
                        username=preferred_name,
                        email=email,
                        defaults={
                            'username': email,
                            'is_superuser': superuser,
                            'is_staff': staff,
                            'email': email
                        }
                    )
            except IntegrityError:
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'is_superuser': superuser,
                        'is_staff': staff,
                        'email': email
                    }
                )

            if not user.is_active:
                user.is_active = True
                user.save()

            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
