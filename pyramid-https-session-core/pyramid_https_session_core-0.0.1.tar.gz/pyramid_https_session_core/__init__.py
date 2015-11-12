from pyramid.interfaces import ISessionFactory
from pyramid.settings import asbool


# ==============================================================================


class ISessionHttpsFactory(ISessionFactory):
    """
    subclass of ISessionFactory; needs to be unique class
    """
    pass


class NotHttpsRequest(Exception):
    """
    Raised when we're not an HTTPS request, and the application is configured 
    to ensure_scheme
    """
    pass


# ------------------------------------------------------------------------------


def request_property__session_https(request):
    """
    Private Method.
    This should be a reified request method. 
    """
    # are we ensuring https?
    if request.registry.settings['pyramid_https_session_core.ensure_scheme']:
        if request.scheme != 'https':
            return None
    factory = request.registry.queryUtility(ISessionHttpsFactory)
    if factory is None:
        raise AttributeError('No `session_https` factory registered')
    return factory(request)


# ------------------------------------------------------------------------------


def register_https_session_factory(config, settings, https_session_factory):
    """
    Plugin Developer Method.
    Developers should call this when creating an ISessionHttpsFactory
    """
    
    def register_session_https_factory():
        config.registry.registerUtility(https_session_factory, ISessionHttpsFactory)

    intr = config.introspectable('session https factory',
                                 None,
                                 config.object_description(https_session_factory),
                                 'session https factory'
                                 )
    intr['factory'] = https_session_factory
    config.action(ISessionHttpsFactory, register_session_https_factory,
                  introspectables=(intr, ),
                  )
    config.set_request_property(request_property__session_https,
                                'session_https', reify=True,
                                )
