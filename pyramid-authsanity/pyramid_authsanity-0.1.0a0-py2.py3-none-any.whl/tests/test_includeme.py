import pytest

from pyramid.authorization import ACLAuthorizationPolicy
import pyramid.testing

from zope.interface import (
    Interface,
    implementedBy,
    providedBy,
)

from zope.interface.verify import (
        verifyClass,
        verifyObject
        )

from pyramid_services import IServiceClassifier

from pyramid_authsanity.interfaces import (
        IAuthSourceService,
        )

class TestAuthServicePolicyIntegration(object):
    @pytest.fixture(autouse=True)
    def pyramid_config(self, request):
        from pyramid.interfaces import IDebugLogger
        self.config = pyramid.testing.setUp()
        self.config.set_authorization_policy(ACLAuthorizationPolicy())

        def finish():
            del self.config
            pyramid.testing.tearDown()
        request.addfinalizer(finish)

    def _makeOne(self, settings):
        self.config.registry.settings.update(settings)
        self.config.include('pyramid_authsanity')

    def test_include_me(self):
        from pyramid_authsanity.policy import AuthServicePolicy
        self._makeOne({})
        self.config.commit()
        introspector = self.config.registry.introspector
        auth_policy = introspector.get('authentication policy', None)

        assert isinstance(auth_policy['policy'], AuthServicePolicy)

        with pytest.raises(ValueError):
            find_service_factory(self.config, IAuthSourceService)

    def test_include_me_cookie_no_secret(self):
        settings = {'authsanity.source': 'cookie'}
        
        with pytest.raises(RuntimeError):
            self._makeOne(settings)

    def test_include_me_cookie_with_secret(self):
        from pyramid_authsanity.policy import AuthServicePolicy
        settings = {'authsanity.source': 'cookie', 'authsanity.secret': 'sekrit'}

        self._makeOne(settings)
        self.config.commit()
        introspector = self.config.registry.introspector
        auth_policy = introspector.get('authentication policy', None)

        assert isinstance(auth_policy['policy'], AuthServicePolicy)
        assert verifyClass(IAuthSourceService, find_service_factory(self.config, IAuthSourceService))

    def test_include_me_session(self):
        from pyramid_authsanity.policy import AuthServicePolicy
        settings = {'authsanity.source': 'session'}

        self._makeOne(settings)
        self.config.commit()
        introspector = self.config.registry.introspector
        auth_policy = introspector.get('authentication policy', None)

        assert isinstance(auth_policy['policy'], AuthServicePolicy)
        assert verifyClass(IAuthSourceService, find_service_factory(self.config, IAuthSourceService))


def find_service_factory(
    config,
    iface=Interface,
    ):

    context_iface = providedBy(None)
    svc_types = (IServiceClassifier, context_iface)

    adapters = config.registry.adapters
    svc_factory = adapters.lookup(svc_types, iface, name='')
    if svc_factory is None:
        raise ValueError('could not find registered service')
    return svc_factory
