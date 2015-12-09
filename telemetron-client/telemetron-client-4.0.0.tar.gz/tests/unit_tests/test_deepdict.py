def test_deep_merge_priority():
    from telemetronclient.utils.deepdict import DeepDict

    defaults = {
        'timer': {
            'tags': {
                'unit': 'ms',
            },
            'agg': ['avg', 'p90', 'count', 'count_ps'],
            'agg_freq': 10,
            'namespace': 'default ns',
            'timestamp': None,
            'unique': 'only in original'
        }
    }

    new = {
        'timer': {
            'tags': {
                'unit': 'overridden_ms',
            },
            'agg': ['overridden_agg'],
            'agg_freq': 10,
            'namespace': 'overridden_ns',
            'timestamp': None
        }
    }

    new2 = {
        'timer': {
            'tags': {
                'unit': 'overridden_ms_new2',
            },
            'unique': 'only in new2'
        }
    }

    res = DeepDict.deep_merge(defaults, new, new2)
    assert res['timer']['tags']['unit'] == new2['timer']['tags']['unit']
    assert res['timer']['unique'] == 'only in new2'
