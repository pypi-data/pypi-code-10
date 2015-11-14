from zerotest.generator.python.render import Renderer
from zerotest.request import Request
from zerotest.response import Response

__author__ = 'Hari Jiang'


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

    assert renderer.render(records) == _RESULT


_RESULT = """
from zerotest.request import Request
from zerotest.response import Response
from zerotest.response_matcher import ResponseMatcher


matcher = ResponseMatcher()
verify_ssl = False


def test_get_root():
    request = Request(headers={'header_1': '1'}, host='for_test.org', path='/', scheme='http', data='just_for_test', method='GET')
    real = Response.from_requests_response(request.send_request(verify=verify_ssl))
    expect = Response(status=200, headers={'content_type': 'text'}, body='ok')
    matcher.match_responses(real, expect)


def test_post_second_request():
    request = Request(headers={'header_a': 'a'}, host='for_test.org', path='/second_request', scheme='https', data='second_request', method='POST')
    real = Response.from_requests_response(request.send_request(verify=verify_ssl))
    expect = Response(status=200, headers={'content_type': 'text'}, body='ok')
    matcher.match_responses(real, expect)

"""
