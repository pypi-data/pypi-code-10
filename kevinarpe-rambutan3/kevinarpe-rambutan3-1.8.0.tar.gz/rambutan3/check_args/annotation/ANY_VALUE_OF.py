from rambutan3.check_args.base.RAnyValueOfMatcher import RAnyValueOfMatcher


# noinspection PyPep8Naming
def ANY_VALUE_OF(*value_tuple) -> RAnyValueOfMatcher:
    x = RAnyValueOfMatcher(*value_tuple)
    return x
