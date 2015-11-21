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


def test_ignore_headers_compare():
    matcher = ResponseMatcher(ignore_headers=['c', 'd', 'e'])
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


def test_ignore_all_headers_compare():
    matcher = ResponseMatcher(ignore_all_headers=True)
    r1 = Response(status=200, headers={"a": "1", "c": "not"}, body="ok")
    r2 = Response(status=200, headers={"a": "1", "c": "same", "d": 3}, body="ok")
    f = lambda: matcher.match_responses(r1, r2)
    assert not raised_error(f, MatchError)


def test_ignore_fields_compare():
    import json
    matcher = ResponseMatcher(ignore_fields=['some_record.created_at', 'id'])
    f = lambda: matcher.match_responses(r1, r2)
    r1 = Response(status=200, headers={}, body=json.dumps({"id": 1, "name": "test"}))
    r2 = Response(status=200, headers={}, body=json.dumps({"id": 2, "name": "test"}))
    # not work if not content-type
    assert raised_error(f, MatchError)
    r1.headers['content-type'] = 'application/json'
    r2.headers['CONTENT-TYPE'] = 'application/json'
    assert not raised_error(f, MatchError)

    r1.body = json.dumps({"some_record.created_at": 'now', 'record': {'created_at': '111'}})
    r2.body = json.dumps({"record": {'created_at': '111'}})
    assert not raised_error(f, MatchError)
    r1.body = json.dumps({"some_record.created_at": 'now', 'some_record': {'created_at': '111'}})
    r2.body = json.dumps({"some_record": {'created_at': '111'}})
    assert raised_error(f, MatchError)

    r1.body = json.dumps({"some_record.created_at": 'now'})
    r2.body = json.dumps({"some_record": {'created_at': '112'}})
    assert raised_error(f, MatchError)

    # test key path under list
    r1.body = json.dumps({"some_record": [{'created_at': '1123', 'id': '0'}]})
    r2.body = json.dumps({"some_record": [{'created_at': '112', 'id': '1'}]})
    assert raised_error(f, MatchError)
    r1.body = json.dumps({"some_record": [{'created_at': '1123', 'id': '0'}, {'created_at': '3322'}]})
    r2.body = json.dumps({"some_record": [{'created_at': '112', 'id': '1'}, {'created_at': 'tomorrow'}]})
    assert raised_error(f, MatchError)

    r1.body = json.dumps({"some_record": [{'created_at': '1123', 'id': '1'}, {'created_at': '3322'}]})
    r2.body = json.dumps({"some_record": [{'created_at': '112', 'id': '1'}, {'created_at': 'tomorrow'}]})
    assert not raised_error(f, MatchError)
