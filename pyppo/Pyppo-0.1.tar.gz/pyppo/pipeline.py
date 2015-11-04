from copy import deepcopy
import functools
from .exceptions import StepValidationError


def validate_with(validate_function=None):
    """
    Functional validation for pipeline steps.
    This function accepts a validation function passed as argument. The validate
    function should verify and check if the correct argguments are being passed
    correctly to the decorated step.

    >>> 
    ... validation = lambda entry: 'x' in entry
    ...
    ... def add_x_to_entry(entry):
    ...     # should add 'x' key to entry dictionary but didn't
    ...     return entry
    ...
    ... @validate_with(validation)
    ... def increment_1_on_x_key(entry):
    ...     entry['x'] += 1
    ...     return entry
    ...
    ... entry = {}
    ... # consume will saise a StepValidationError
    ... consume(pipeline([entry], [add_x_to_entry, increment_1_on_x_key]))
    ...
    """

    def function_decorator(fn):
        def decorated(*args, **kwargs):

            if not validate_function(*args, **kwargs):
                raise StepValidationError
            else:
                return fn(*args, **kwargs)

        return decorated
    return function_decorator


def consume(iterator):
    for _ in iterator:
        pass


def pipeline(source, *steps):
    """
    Higher order function to abstract generators from the steps.

        Pipelines can be represented by a series of steps as shown on the
    following example:

    :::
    >>> 
    ... obj = []
    ...
    ... def do_something(obj):
    ...     obj.append(1)
    ...     return obj
    ...
    ... def do_something_else(obj):
    ...     obj.append(2)
    ...     return obj
    ...
    ... consume(pipeline([obj], [do_something, do_something_else]))
    ...
    ... print obj
    ... [1, 2]

    """
    for entry in source:
        yield functools.reduce(lambda entry, step: step(entry), steps, entry)


def fork(*branches):
    """
    fork(*branches) will fork the pipeline into the specified branches.
    branches are a list of pipeline steps
    :::
    >>> 
    ... obj = []
    ... def first_step(obj):
    ...     obj.append(1)
    ...     return obj
    ...
    ... def branch_add_two(obj):
    ...     obj.append(2)
    ...     return obj
    ...
    ... def branch_add_four(obj):
    ...     obj.append(4)
    ...     return obj
    ...
    ... pipeline([obj], first_step, fork([branch_add_two], [branch_add_four]))
    ...
    """
    def decorated(entry):

        for branch in branches:
            consume(functools.partial(pipeline, [deepcopy(entry)])(*branch))
        return entry

    return decorated
