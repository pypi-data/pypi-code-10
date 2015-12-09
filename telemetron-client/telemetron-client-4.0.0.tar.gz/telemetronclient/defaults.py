"""
Defaults module
"""
import logging


METHOD_DEFAULTS = {
    'timer': {
        'tags': {
            'unit': 'ms',
        },
        'agg': ['avg', 'p90', 'count', 'count_ps'],
        'agg_freq': 10,
        'namespace': 'application',
        'timestamp': None
    },
    'counter': {
        'tags': {
        },
        'agg': ['avg', 'p90', 'count_ps'],
        'agg_freq': 10,
        'namespace': 'application',
        'timestamp': None
    },
    'gauge': {
        'tags': {
            },
        'agg': ['last'],
        'agg_freq': 10,
        'namespace': 'application',
        'timestamp': None
    },
    '_put': {
        'tags': {
            },
        'agg': [],
        'agg_freq': 10,
        'namespace': 'application',
        'timestamp': None
    }
}

DEFAULT_SETTINGS = {
    'host': '127.0.0.1',
    'port': 2013,
    'prefix': None,
    'transport': None,
    'secure': True,
    'timeout': 2000.0,
    'token': None,
    'app': None,
    'dryrun': False,
    'logger': logging.getLogger('telemetronclient'),
    'tags': {},
    'sample_rate': 100,
    'flush_size': 10,
    'namespace': 'application'
    }
