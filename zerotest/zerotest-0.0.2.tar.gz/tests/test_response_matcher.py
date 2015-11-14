__author__ = 'Hari Jiang'
from zerotest.response import Response
from zerotest.response_matcher import ResponseMatcher, MatchError


def raised_error(func, err_type):
    raised = False
    try:
        func()
    except err_type:
        raised = True

    return raised


def test_compare():
    matcher = ResponseMatcher()
    r1 = Response(status=200, headers={"a": "1"}, body="ok")
    r2 = Response(status=200, headers={"a": "1"}, body="ok")
    f = lambda: matcher.match_responses(r1, r2)
    assert not raised_error(f, MatchError)
    r2.body = "not ok"
    assert raised_error(f, MatchError)
    r2.body = "ok"
    r2.status = 201
    assert raised_error(f, MatchError)
    r2.status = 200
    r2.headers['b'] = 2
    assert raised_error(f, MatchError)
    del r2.headers['b']
    assert not raised_error(f, MatchError)


def test_ignore_header_compare():
    matcher = ResponseMatcher(['c', 'd', 'e'])
    r1 = Response(status=200, headers={"a": "1", "c": "not"}, body="ok")
    r2 = Response(status=200, headers={"a": "1", "c": "same"}, body="ok")
    f = lambda: matcher.match_responses(r1, r2)
    assert not raised_error(f, MatchError)
    r1.headers['d'] = "ignored should"
    assert not raised_error(f, MatchError)
    r2.headers['e'] = "ignored should"
    assert not raised_error(f, MatchError)
    r1.headers['g'] = "not ignored"
    assert raised_error(f, MatchError)
