#!/usr/bin/env python
import json_compare


def test_list_of_hashes():
    a = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    b = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert json_compare.are_same(a, b)[0]


def test_list_of_hashes_unordered():
    a = [
        {"wtf1": "omg1"},
        {"wtf": "omg"}
    ]
    b = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert json_compare.are_same(a, b, True)[0]


def test_list_of_hashes_unordered_fail():
    a = [
        {"wtf1": "omg1"},
        {"wtf": "omg"}
    ]
    b = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert not json_compare.are_same(a, b)[0]


def test_list_of_hashes_ignore_key():
    a = [
        {"wtf1": "omg1"},
        {"wtf2": "omg"}
    ]
    b = [
        {"wtf1": "omg1"},
        {"wtf2": "omg3"}
    ]
    assert json_compare.are_same(a, b, True, ["wtf2"])[0]


def test_hash_list_of_hashes_unordered():
    a = {
        "wtf": [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
    }
    b = {
        "wtf": [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
    }
    assert json_compare.are_same(a, b, True)[0]


def test_hash_list_of_hashes_unordered_fail():
    a = {
        "wtf": [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
    }
    b = {
        "wtf": [
            {"wtf": "omg"},
            {"wtf1": "omg1"}
        ]
    }
    assert not json_compare.are_same(a, b)[0]


def test_hash_vs_list_fail():
    a = {
        "wtf": [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
    }
    b = [
        {"wtf1": "omg1"}
    ]
    assert not json_compare.are_same(a, b)[0]


def test_list_vs_hash_fail():
    a = [
        {"wtf1": "omg1"}
    ]
    b = {
        "wtf": [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
    }
    assert not json_compare.are_same(a, b)[0]


def test_hash_vs_list_size_fail():
    a = {
        "wtf": [
            {"wtf1": "omg1"},
            {"wtf": "omg"}
        ]
    }
    b = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert not json_compare.are_same(a, b)[0]


def test_nested_list_order_sensitivity_false():
    a = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be null"
            },
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            }
        ]
    }
    b = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            },
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be null"
            }
        ]
    }
    assert not json_compare.are_same(a, b)[0]


def test_nested_list_order_sensitivity():
    a = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be null"
            },
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            }
        ]
    }
    b = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            },
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be null"
            }
        ]
    }
    assert json_compare.are_same(a, b, True)[0]


def test_inner_val_sensitivity_false():
    a = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be smelly"
            },
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            }
        ]
    }
    b = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be null"
            },
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            }
        ]
    }
    assert not json_compare.are_same(a, b, True)[0]


def test_nested_list_order_inner_val_sensitivity_false():
    a = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be smelly"
            },
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            }
        ]
    }
    b = {
        "failureReason": "Invalid request entity",
        "fieldValidationErrors": [
            {
                "field": "Catalog.name",
                "reason": "may not be null"
            },
            {
                "field": "Catalog.catalogOwner",
                "reason": "may not be null"
            }
        ]
    }
    assert not json_compare.are_same(a, b, True)[0]


def test_giant_json_ignores_reordering():
    a = open("testing-data/jsonbloba.json").read()
    b = open("testing-data/jsonblobb.json").read()
    assert json_compare.json_are_same(a, b, True)[0]


def test_giant_json_finds_reordering():
    a = open("testing-data/jsonbloba.json").read()
    b = open("testing-data/jsonblobb.json").read()
    assert not json_compare.json_are_same(a, b)[0]


# Test two json that are same size and keys/values match
def test_contains_same_size():
    actual = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    expected = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert json_compare.contains(expected, actual)[0]


# Test two json that are same size and keys/values match with ignore_order
def test_contains_same_size2():
    actual = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    expected = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert json_compare.contains(expected, actual, True)[0]


# Test two json that are same size but values do not match
def test_contains_same_size3():
    actual = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    expected = [
        {"wtf": "omg"},
        {"wtf1": "omg999999"}
    ]
    assert not json_compare.contains(expected, actual)[0]


# Test two json that are same size but keys do not match
def test_contains_same_size4():
    actual = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    expected = [
        {"wtf": "omg"},
        {"wtf999": "omg1"}
    ]
    assert not json_compare.contains(expected, actual)[0]


# Test two json where Actual is larger - it can (potentialy) contain all of the expected attributes
def test_contains_actual_bigger():
    actual = [
        {"wtf": "omg"},
        {"wtf1": "omg1"},
        {"wtf3": "omg3"}
    ]
    expected = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    assert json_compare.contains(expected, actual)[0]


# Test two json where Actual is smaller - it can NOT contain all of expected attributes
def test_contains_actual_smaller():
    actual = [
        {"wtf": "omg"},
        {"wtf1": "omg1"}
    ]
    expected = [
        {"wtf": "omg"},
        {"wtf1": "omg1"},
        {"wtf2": "omg2"}
    ]
    assert not json_compare.contains(expected, actual)[0]


def test_int_within_range():
    actual = [
        {"wtf": 5},
        {"wtf1": 6}
    ]
    expected = [
        {"wtf": 9},
        {"wtf1": 4}
    ]
    assert json_compare.are_same(expected, actual, times_higher=2, times_lower=.5)[0]


def test_int_outside_range():
    actual = [
        {"wtf": 11},
        {"wtf1": 2}
    ]
    expected = [
        {"wtf": 5},
        {"wtf1": 6}
    ]
    assert not json_compare.are_same(expected, actual, times_higher=2, times_lower=.5)[0]


def test_float_within_range():
    actual = [
        {"wtf": 15.3},
        {"wtf1": 5.5}
    ]
    expected = [
        {"wtf": 5.5},
        {"wtf1": 6.6}
    ]
    assert json_compare.are_same(expected, actual, times_higher=3, times_lower=.6)[0]


def test_float_outside_range():
    actual = [
        {"wtf": 18.3},
        {"wtf1": 2.5}
    ]
    expected = [
        {"wtf": 5.5},
        {"wtf1": 6.6}
    ]
    assert not json_compare.are_same(expected, actual, times_higher=3, times_lower=.6)[0]


def test_float_int_compare():
    actual = [
        {"wtf": 12.3},
        {"wtf1": 5}
    ]
    expected = [
        {"wtf": 5},
        {"wtf1": 6.6}
    ]
    assert json_compare.are_same(expected, actual, times_higher=3, times_lower=.6, compare_ints_floats=True)[0]


def test_expected_zero_has_range():
    actual = [
        {"wtf": 1},
        {"wtf1": 7}
    ]
    expected = [
        {"wtf": 0},
        {"wtf1": 6}
    ]
    assert json_compare.are_same(expected, actual, times_higher=3, times_lower=.6, compare_ints_floats=True)[0]
