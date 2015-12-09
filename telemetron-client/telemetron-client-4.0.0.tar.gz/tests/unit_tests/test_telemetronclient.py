from nose.tools import assert_raises


def test_expect_buffer_to_empty_on_flush():
    from telemetronclient.telemetronclient import TelemetronClient

    def buffer_to_empty_on_flush(transport):
        client = TelemetronClient(settings={
            'dryrun': True,
            'prefix': 'prefix',
            'transport': transport,
            'app': 'app',
            'host': 'localhost',
            'port': 2013,
            'flush_size': 999
            })

        client.counter("inc1", 2)
        assert client.buffer_count == 1
        client.flush()
        assert client.buffer_count == 0

    for transport in TelemetronClient.VALID_TRANSPORTS:
        yield buffer_to_empty_on_flush, transport


def test_expect_overriding_defaults():
    def defaults_override(method):
        from telemetronclient.telemetronclient import TelemetronClient
        from telemetronclient.utils.map import Map

        import re

        settings = {
            'dryrun': True,
            'prefix': '%s_prefix' % (method,),
            'transport': 'udp'
            }

        defaults = {
            method: {
                'agg': ['avg'],
                'agg_freq': 11,
                'namespace': '%s_ns' % (method,)
                }
            }

        client = TelemetronClient(settings=settings, defaults=defaults)

        func = getattr(client, method)
        func("%s1" % (method,), 999)
        pat = r"%(method)s_prefix.%(method)s_ns.%(method)s.%(method)s1.* 999 .* "+\
            "avg,11 100"
        pat = pat % {'method': method}

        assert re.match(pat, client._buffer[0]) is not None

    for i in ["timer", "gauge", "counter"]:
        yield defaults_override, i


def test_expect_exception_on_missing_required_arguments():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError
    from telemetronclient.utils.map import Map

    assert_raises(
        TelemetronValueError,
        TelemetronClient,
        settings=Map({'dryrun': True, 'prefix': 'prefix'})
        )

    assert_raises(
        TelemetronValueError,
        TelemetronClient,
        settings=Map({'dryrun': True, 'transport': 'udp'})
        )


def test_expect_exception_on_incorrect_transport():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError

    assert_raises(
        TelemetronValueError,
        TelemetronClient,
        settings={'transport': 'invalid', 'prefix': 'prefix'}
        )


def test_expect_not_to_raise_exception_on_transport_end():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError

    settings = {'transport': 'udp', 'prefix': 'prefix'}
    client = TelemetronClient(settings=settings)
    client.end_transport()


def test_expect_exception_on_incorrect_sample_rate():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError

    assert_raises(
        TelemetronValueError,
        TelemetronClient,
        settings={'dryrun': True, 'prefix': 'prefix', 'transport': 'udp',
                  'sample_rate': 101}
        )

    settings = {'transport': 'udp', 'prefix': 'prefix'}
    client = TelemetronClient(settings=settings)

    assert_raises(
        TelemetronValueError,
        client.put,
        'metric', 10, tags={}, sample_rate=101)


def test_expect_global_tags_to_be_used():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.utils.map import Map

    c = TelemetronClient(settings=Map({
        'dryrun': True,
        'prefix': 'test_prefix',
        'transport': 'udp',
        'app': 'test_app',
        'tags': {'global1': 'foo'}}))

    must_exist = ('app', 'client', 'global1')
    assert all([k in c.global_tags for k in must_exist])


def test_expect_put_raw_to_append_lines_to_buffer():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError

    settings = {'transport': 'udp', 'prefix': 'prefix', 'flush_size': 10}
    client = TelemetronClient(settings=settings)
    client.put_raw(["line%d" % (r,) for r in range(9)])
    assert client.buffer_count == 9


def test_expect_put_raw_flush_buffer_with_multiple_lines():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError

    settings = {'transport': 'udp', 'prefix': 'prefix', 'flush_size': 8,
                'dryrun': True}
    client = TelemetronClient(settings=settings)
    client.put_raw(["line%d" % (r,) for r in range(9)])
    assert client.buffer_count == 1


def test_expect_stats_line_in_buffer():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.telemetronclient import TelemetronValueError

    settings = {'transport': 'udp', 'prefix': 'prefix', 'flush_size': 8,
                'dryrun': True}
    client = TelemetronClient(settings=settings, system_stats=True)
    client.put_raw(["line%d" % (r,) for r in range(8)])
    lines = [sent[0][0] for sent in client._socket.sent]
    assert len([line for line in lines if "buffer.flush_length" in line]) == 1


def test_expect_settings_map_from_dict():
    from telemetronclient.telemetronclient import TelemetronClient
    from telemetronclient.utils.map import Map

    c = TelemetronClient(settings={
        'dryrun': True,
        'prefix': 'test_prefix',
        'transport': 'udp',
        'app': 'test_app'
        })

    assert isinstance(c._settings, Map)
