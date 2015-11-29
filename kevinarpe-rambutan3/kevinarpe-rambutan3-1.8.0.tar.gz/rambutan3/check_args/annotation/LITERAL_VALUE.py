from rambutan3.check_args.base.RAnyValueOfMatcher import RAnyValueOfMatcher


# noinspection PyPep8Naming
def LITERAL_VALUE(value) -> RAnyValueOfMatcher:
    x = RAnyValueOfMatcher(value)
    return x
