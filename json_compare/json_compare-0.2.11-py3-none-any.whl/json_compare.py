import rapidjson
import sys
from collections import OrderedDict


if sys.version_info[0] < 3:
    from future import range
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    from .is_close import isclose
else:
    from math import isclose


class Stack:
    def __init__(self):
        self.stack_items = []

    def append(self, stack_item):
        self.stack_items.append(stack_item)
        return self

    def __repr__(self):
        stack_dump = ''
        for item in self.stack_items:
            stack_dump += str(item)
        return stack_dump

    def __str__(self):
        stack_dump = ''
        for item in self.stack_items:
            stack_dump += str(item)
        return stack_dump


class StackItem:
    def __init__(self, reason, expected, actual):
        self.reason = reason
        self.expected = expected
        self.actual = actual

    def __repr__(self):
        return 'Reason: {0}\nExpected:\n{1}\nActual:\n{2}'.format(self.reason, _format_value(self.expected),
                                                                  _format_value(self.actual))

    def __str__(self):
        return '\n\nReason: {0}\nExpected:\n{1}\nActual:\n{2}'.format(self.reason, _format_value(self.expected),
                                                                      _format_value(self.actual))


def _indent(s):
    return '\n'.join('  ' + line for line in s.splitlines())


def _format_value(value):
    return _indent(_generate_pprint_json(value))


def _generate_pprint_json(value):
    return rapidjson.dumps(value, indent=4)


def _is_dict_same(expected, actual, ignore_value_of_keys, greater_than=1, less_than=1, compare_ints_floats=False):
    # DAN - I had to flip flop this
    for key in expected:
        if key not in actual:
            return False, Stack().append(
                StackItem('Expected key "{0}" Missing from Actual'.format(key), expected, actual))

        if key not in ignore_value_of_keys:
            # have to change order
            # are_same_flag, stack = _are_same(actual[key], expected[key], ignore_value_of_keys)
            are_same_flag, stack = _are_same(expected[key], actual[key], ignore_value_of_keys, False,
                                             greater_than, less_than, compare_ints_floats)
            if not are_same_flag:
                return False, stack.append(StackItem('Different values', expected[key], actual[key]))
    return True, Stack()


def _is_list_same(expected, actual, ignore_value_of_keys, greater_than=1, less_than=1, compare_ints_floats=False):
    for i in range(len(expected)):
        are_same_flag, stack = _are_same(expected[i], actual[i], ignore_value_of_keys, False, greater_than, less_than,
                                         compare_ints_floats)
        if not are_same_flag:
            return False, stack.append(StackItem('Different values (Check order)', expected[i], actual[i]))
    return True, Stack()


def _bottom_up_sort(unsorted_json):
    if isinstance(unsorted_json, dict):
        return sorted((k, _bottom_up_sort(v)) for k, v in unsorted_json.items())
    if isinstance(unsorted_json, list):
        return sorted(_bottom_up_sort(x) for x in unsorted_json)
    else:
        return unsorted_json


def _to_ordered_dict(sorted_json):
    if isinstance(sorted_json, list):
        ordered = OrderedDict()
        if sorted_json and isinstance(sorted_json[0], list):
            ordered = []
            for i in sorted_json:
                ordered.append(_to_ordered_dict(i))
            return ordered
        else:
            for i in sorted_json:
                if isinstance(i, list):
                    ordered.update(_to_ordered_dict(i))
                elif isinstance(i, tuple):
                    ordered[i[0]] = _to_ordered_dict(i[1])
            return ordered
    else:
        return sorted_json


def _are_same(expected, actual, ignore_value_of_keys, ignore_missing_keys=False, rel_tolerance=0, abs_tolerance=0,
              compare_ints_floats=False):
    # Check for None
    if expected is None:
        return expected == actual, Stack()

    # Ensure they are of same type
    if type(expected) != type(actual):
        if compare_ints_floats and type(expected) in (int, float) and type(actual) in (int, float):
            pass
        else:
            return False, Stack().append(
                StackItem('Type Mismatch: Expected Type: {0}, Actual Type: {1}'.format(type(expected), type(actual)),
                          expected, actual))

    # Compare primitive types immediately
    if type(expected) in (str, bool):
        return expected == actual, Stack()
    elif type(expected) in (int, float):
        if rel_tolerance != 1 or abs_tolerance != 1:
            return isclose(expected, actual, rel_tol=rel_tolerance, abs_tol=abs_tolerance), Stack()
        else:
            return expected == actual, Stack()

    # Ensure collections have the same length (if applicable)
    if ignore_missing_keys:
        # Ensure collections has minimum length (if applicable) 
        # This is a short-circuit condition because (b contains a)
        if len(expected) > len(actual):
            return False, Stack().append(StackItem(
                'Length Mismatch: Minimum Expected Length: {0}, Actual Length: {1}'.format(len(expected), len(actual)),
                expected, actual))

    else:
        # Ensure collections has same length
        if len(expected) != len(actual):
            return False, Stack().append(StackItem(
                'Length Mismatch: Expected Length: {0}, Actual Length: {1}'.format(len(expected), len(actual)),
                expected, actual))

    if isinstance(expected, dict) or isinstance(expected, OrderedDict):
        return _is_dict_same(expected, actual, ignore_value_of_keys, rel_tolerance, abs_tolerance, compare_ints_floats)

    if isinstance(expected, list):
        return _is_list_same(expected, actual, ignore_value_of_keys, rel_tolerance, abs_tolerance, compare_ints_floats)

    return False, Stack().append(StackItem('Unhandled Type: {0}'.format(type(expected)), expected, actual))


def are_same(original_a, original_b, ignore_list_order_recursively=False, ignore_value_of_keys=[], rel_tolerance=1,
             abs_tolerance=1, compare_ints_floats=False):
    if ignore_list_order_recursively:
        a = _to_ordered_dict(_bottom_up_sort(original_a))
        b = _to_ordered_dict(_bottom_up_sort(original_b))
    else:
        a = original_a
        b = original_b
    return _are_same(a, b, ignore_value_of_keys, False, rel_tolerance, abs_tolerance, compare_ints_floats)


def contains(expected_original, actual_original, ignore_list_order_recursively=False, ignore_value_of_keys=[],
             compare_ints_floats=False):
    if ignore_list_order_recursively:
        actual = _to_ordered_dict(_bottom_up_sort(actual_original))
        expected = _to_ordered_dict(_bottom_up_sort(expected_original))
    else:
        actual = actual_original
        expected = expected_original
    return _are_same(expected, actual, ignore_value_of_keys, True, compare_ints_floats=compare_ints_floats)


def json_are_same(a, b, ignore_list_order_recursively=False, ignore_value_of_keys=[], rel_tolerance=1, abs_tolerance=1,
                  compare_ints_floats=False):
    return are_same(rapidjson.loads(a), rapidjson.loads(b), ignore_list_order_recursively, ignore_value_of_keys,
                    rel_tolerance,
                    abs_tolerance, compare_ints_floats)
