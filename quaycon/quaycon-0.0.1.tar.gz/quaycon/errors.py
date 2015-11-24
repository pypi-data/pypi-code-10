class QuayConError(Exception):
    pass


class MissingTokenError(QuayConError):
    def __init__(self, organization):
        self.organization = organization
        msg = u"Missing 'token' for organization: {}".format(organization)
        super(MissingTokenError, self).__init__(msg)


class UnknownOrganization(QuayConError):
    def __init__(self, organization):
        self.organization = organization
        msg = u'Unknown organization: {}'.format(organization)
        super(UnknownOrganization, self).__init__(msg)


class ImageError(QuayConError):
    def __init__(self, org, name, *args, **kwargs):
        super(ImageError, self).__init__(*args, **kwargs)
        self.org = org
        self.name = name


class UnknownBuildTrigger(ImageError):
    def __init__(self, org, name, trigger_uuid):
        self.trigger_uuid = trigger_uuid
        msg = "Unknown build trigger for {}/{}: {}".format(
            org, name, trigger_uuid
        )
        super(UnknownBuildTrigger, self).__init__(org, name, msg)


class UnknownRepository(ImageError):
    def __init__(self, org, name):
        msg = u'Unknown repository {}/{}'.format(org, name)
        super(UnknownRepository, self).__init__(org, name, msg)


class UnsupportedRegistry(QuayConError):
    def __init__(self, registry, message):
        if registry is None:
            registry = 'Docker Hub'
        msg = "{}: {}".format(message, registry)
        super(UnsupportedRegistry, self).__init__(msg)
