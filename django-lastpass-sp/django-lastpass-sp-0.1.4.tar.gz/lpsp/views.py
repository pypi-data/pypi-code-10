from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse

from saml_service_provider import views as samlviews
from .settings import LastPassServiceProviderSettings


def proxy_port(f):
    '''
    Patch saml_service_provider port setting

    saml_service_provider trusts too much in X-Forwarded-Port header
    and sets server port to local port if the header is missing.

    onelogin.saml2 explicitly sets the port eagerly.

    This results in some proxies being missed.

    This peeks common de facto reverse proxy headers and guesses
    the public port accordingly.
    '''
    @wraps(f)
    def wrapped(self, request, *f_args, **f_kwargs):
        if 'HTTP_X_FORWARDED_PORT' not in request.META:
            proto = request.META.get('HTTP_X_FORWARDED_PROTO', None)

            if 'HTTP_X_FORWARDED_FOR' in request.META:
                request.META['HTTP_X_FORWARDED_PORT'] = '80'

            if proto == 'https':
                request.META['HTTP_X_FORWARDED_PORT'] = '443'
            if proto == 'http':
                request.META['HTTP_X_FORWARDED_PORT'] = '80'

            if 'HTTP_X_FORWARDED_HOST' in request.META:
                try:
                    fwd_host = request.META['HTTP_X_FORWARDED_HOST']
                    port = int(fwd_host.rsplit(':', 1))
                    request.META['HTTP_X_FORWARDED_PORT'] = port
                except (ValueError, IndexError):
                    pass

            print request.META['HTTP_X_FORWARDED_PORT']

        return f(self, request, *f_args, **f_kwargs)
    return wrapped


class SettingsMixin(object):
    def get_onelogin_settings(self):
        conf = dict()
        conf['onelogin_connector_id'] = settings.LASTPASS_CONNECTOR_ID
        if hasattr(settings, 'LASTPASS_CERTIFICATE'):
            conf['onelogin_x509_cert'] = settings.LASTPASS_CERTIFICATE
        elif hasattr(settings, 'LASTPASS_CERTIFICATE_FILE'):
            with open(settings.LASTPASS_CERTIFICATE_FILE, 'rb') as cert:
                conf['onelogin_x509_cert'] = cert.read()
        else:
            conf['onelogin_x509_fingerprint'] = settings.LASTPASS_FINGERPRINT

        hostname = getattr(settings, 'LASTPASS_HOSTNAME', 'http://localhost:8000')

        conf['sp_metadata_url'] = hostname + reverse('saml_metadata')
        conf['sp_login_url'] = hostname + reverse('saml_login_complete')
        conf['sp_logout_url'] = hostname + reverse('logout')
        conf['debug'] = settings.DEBUG
        conf['strict'] = not settings.DEBUG

        if hasattr(settings, 'SAML_SP_CERTIFICATE'):
            conf['sp_x509cert'] = settings.SAML_SP_CERTIFICATE
        else:
            with open(settings.SAML_SP_CERTIFICATE_FILE, 'rb') as cert:
                conf['sp_x509cert'] = cert.read()

        if hasattr(settings, 'SAML_SP_KEY'):
            conf['sp_private_key'] = settings.SAML_SP_KEY
        else:
            with open(settings.SAML_SP_KEY_FILE, 'rb') as key:
                conf['sp_private_key'] = key.read()

        if hasattr(settings, 'SAML_SP_CONTACT_INFO'):
            conf['contact_info'] = settings.SAML_SP_CONTACT_INFO

        if hasattr(settings, 'SAML_SP_ORGANIZATION_INFO'):
            conf['organization_info'] = settings.SAML_SP_ORGANIZATION_INFO

        return LastPassServiceProviderSettings(**conf).settings


class InitiateAuthenticationView(SettingsMixin,
                                 samlviews.InitiateAuthenticationView):
    @proxy_port
    def get(self, request, *args, **kwargs):
        return super(InitiateAuthenticationView, self).get(request, *args, **kwargs)


class CompleteAuthenticationView(SettingsMixin,
                                 samlviews.CompleteAuthenticationView):
    @proxy_port
    def post(self, request, *args, **kwargs):
        return super(CompleteAuthenticationView, self).post(request, *args, **kwargs)


class MetadataView(SettingsMixin,
                   samlviews.MetadataView):
    @proxy_port
    def get(self, request, *args, **kwargs):
        return super(InitiateAuthenticationView, self).get(request, *args, **kwargs)
