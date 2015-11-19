# -*- coding: utf-8 -*-


def create_transport(gribble_config, logger):
    """Creates and returns a transport object"""
    transport_str = gribble_config.get('transport')
    if '.' not in transport_str:
        # allow simple names like 'redis' to load a gribble built-in transport
        module_path = 'gribble.transports.%s_transport' % transport_str.lower()
        class_name = '%sTransport' % transport_str.title()
    else:
        # allow dotted path names to load a custom transport class
        try:
            module_path, class_name = transport_str.rsplit('.', 1)
        except ValueError:
            raise Exception('Invalid transport {0}'.format(gribble_config.get('transport')))

    _module = __import__(module_path, globals(), locals(), class_name, -1)
    transport_class = getattr(_module, class_name)
    transport = transport_class(gribble_config=gribble_config, logger=logger)

    return transport
