from zerotest.generator.python.render import Renderer
from zerotest.request import Request
from zerotest.response import Response


def test_renderer():
    options = dict()
    match_options = dict()
    records = list()
    records.append((Request(scheme='http', method='GET', host='for_test.org', path='/',
                            headers=dict(header_1='1'), data='just_for_test'),
                    Response(status=200, headers=dict(content_type="text"), body='ok')))
    records.append((Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                            headers=dict(header_a='a'), data='second_request'),
                    Response(status=200, headers=dict(content_type="text"), body='ok')))
    renderer = Renderer(options=options, match_options=match_options)

    cases = [
        dict(request=Request(scheme='http', method='GET', host='for_test.org', path='/',
                             headers=dict(header_1='1'), data='just_for_test')
             , response=Response(status=200, headers=dict(content_type="text"), body='ok')
             , func_name='get_root'),
        dict(request=Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                             headers=dict(header_a='a'), data='second_request')
             , response=Response(status=200, headers=dict(content_type="text"), body='ok')
             , func_name='post_second_request'),
    ]

    assert renderer.prepare(records) == cases


def test_renderer_with_options():
    options = dict(endpoint='http://test.com')
    match_options = dict()
    records = list()
    records.append((Request(scheme='http', method='GET', host='for_test.org', path='/',
                            headers=dict(header_1='1'), data='just_for_test'),
                    Response(status=200, headers=dict(content_type="text"), body='ok')))
    records.append((Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                            headers=dict(header_a='a'), data='second_request'),
                    Response(status=200, headers=dict(content_type="text"), body='ok')))
    renderer = Renderer(options=options, match_options=match_options)

    cases = [
        dict(request=Request(scheme='http', method='GET', host='for_test.org', path='/',
                             headers=dict(header_1='1'), data='just_for_test')
             , response=Response(status=200, headers=dict(content_type="text"), body='ok')
             , func_name='get_root'),
        dict(request=Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                             headers=dict(header_a='a'), data='second_request')
             , response=Response(status=200, headers=dict(content_type="text"), body='ok')
             , func_name='post_second_request'),
    ]

    assert renderer.prepare(records) == cases


def test_renderer_with_ignore_headers():
    options = dict()
    match_options = dict(ignore_headers=('date', 'auth'))
    records = list()
    records.append((Request(scheme='http', method='GET', host='for_test.org', path='/',
                            headers=dict(header_1='1'), data='just_for_test'),
                    Response(status=200, headers=dict(content_type="text", date='yesterday', auth='secret'),
                             body='ok')))
    records.append((Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                            headers=dict(header_a='a'), data='second_request'),
                    Response(status=200, headers=dict(content_type="text", date='today'), body='ok')))
    renderer = Renderer(options=options, match_options=match_options)

    cases = [
        dict(request=Request(scheme='http', method='GET', host='for_test.org', path='/',
                             headers=dict(header_1='1'), data='just_for_test')
             , response=Response(status=200, headers=dict(content_type="text"), body='ok')
             , func_name='get_root'),
        dict(request=Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                             headers=dict(header_a='a'), data='second_request')
             , response=Response(status=200, headers=dict(content_type="text"), body='ok')
             , func_name='post_second_request'),
    ]

    assert renderer.prepare(records) == cases


def test_renderer_with_ignore_all_headers():
    options = dict()
    match_options = dict(ignore_all_headers=True)
    records = list()
    records.append((Request(scheme='http', method='GET', host='for_test.org', path='/',
                            headers=dict(header_1='1'), data='just_for_test'),
                    Response(status=200, headers={"content-type": "text", "date": 'yesterday', "auth": 'secret'},
                             body='ok')))
    records.append((Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                            headers=dict(header_a='a'), data='second_request'),
                    Response(status=200, headers={"content-type": "text", "date": 'today'}, body='ok')))
    renderer = Renderer(options=options, match_options=match_options)

    cases = [
        dict(request=Request(scheme='http', method='GET', host='for_test.org', path='/',
                             headers=dict(header_1='1'), data='just_for_test')
             , response=Response(status=200, headers={"content-type": "text"}, body='ok')
             , func_name='get_root'),
        dict(request=Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                             headers=dict(header_a='a'), data='second_request')
             , response=Response(status=200, headers={"content-type": "text"}, body='ok')
             , func_name='post_second_request'),
    ]

    assert renderer.prepare(records) == cases

    options = dict()
    match_options = dict(ignore_all_headers=True)
    records = list()
    records.append((Request(scheme='http', method='GET', host='for_test.org', path='/',
                            headers=dict(header_1='1'), data='just_for_test'),
                    Response(status=200, headers={"date": 'yesterday', "auth": 'secret'},
                             body='ok')))
    records.append((Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                            headers=dict(header_a='a'), data='second_request'),
                    Response(status=200, headers={"date": 'today'}, body='ok')))
    renderer = Renderer(options=options, match_options=match_options)

    cases = [
        dict(request=Request(scheme='http', method='GET', host='for_test.org', path='/',
                             headers=dict(header_1='1'), data='just_for_test')
             , response=Response(status=200, headers={}, body='ok')
             , func_name='get_root'),
        dict(request=Request(scheme='https', method='POST', host='for_test.org', path='/second_request',
                             headers=dict(header_a='a'), data='second_request')
             , response=Response(status=200, headers={}, body='ok')
             , func_name='post_second_request'),
    ]

    assert renderer.prepare(records) == cases
