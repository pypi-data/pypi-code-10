import aioxmpp.service
import aioxmpp.disco as disco


def build_identities_string(identities):
    identities = [
        "/".join(
            str(part) if part is not None else ""
            for part in identity
        )
        for identity in identities
    ]

    if len(set(identities)) != len(identities):
        raise ValueError("duplicate identity")

    identities.sort()
    identities.append("")
    return "<".join(identities)


def build_features_string(features):
    features = list(features)

    if len(set(features)) != len(features):
        raise ValueError("duplicate feature")

    features.sort()
    features.append("")
    return "<".join(features)


class Service(aioxmpp.service.Service):
    ORDER_AFTER = {disco.Service}

    def __init__(self, node):
        super().__init__(node)

        node.stream.service_inbound_presence_filter.register(
            self.handle_inbound_presence,
            type(self)
        )

    def handle_inbound_presence(self, presence):
        presence.xep0115_caps = None
        return presence
