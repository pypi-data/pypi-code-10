import types
from rambutan3.check_args.base.RInstanceWithPredicateMatcher import RInstanceWithPredicateMatcher
from rambutan3.string.RMessageText import RMessageText


# noinspection PyPep8Naming
def INSTANCE_OF_WITH_PREDICATE(predicate_func: types.FunctionType,
                               predicate_description: RMessageText,
                               *class_or_type_tuple) -> RInstanceWithPredicateMatcher:

    x = RInstanceWithPredicateMatcher(predicate_func, predicate_description, *class_or_type_tuple)
    return x
