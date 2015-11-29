import threading
from rambutan3 import RArgs
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.base.traverse.RTypeMatcherTraversePathStepEnum import RTypeMatcherTraversePathStepEnum
from rambutan3.container.frozendict import frozendict
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RDictMatcher import RDictMatcher
from rambutan3.string import RStrUtil
from rambutan3.string.RMessageText import RMessageText


class RDictWhereMatcher(RDictMatcher):

    def __init__(self, dict_enum: RDictEnum, matcher_dict: dict, *, is_exact: bool):
        super().__init__(dict_enum)
        RArgs.check_is_instance(matcher_dict, dict, "matcher_dict")
        RArgs.check_is_instance(is_exact, bool, "is_exact")

        for key, value_matcher in matcher_dict.items():
            RArgs.check_is_instance(value_matcher, RAbstractTypeMatcher, "value_matcher for key '{}'", key)

        self.__matcher_dict = frozendict(matcher_dict)
        self.__is_exact = is_exact

    __sentinel = object()

    # @override
    def matches(self, d: dict, matcher_error: RTypeMatcherError=None) -> bool:
        if not super().matches(d, matcher_error):
            return False

        # Shallow copy is safe here, as we do not modify the values.
        dict_copy = d.copy()
        missing_key_set = self.__get_empty_threadlocal_missing_key_set()
        has_matcher_failed = False

        for key, value_matcher in self.__matcher_dict.items():
            value = dict_copy.get(key, self.__sentinel)

            if self.__sentinel == value:
                missing_key_set.add(key)
                continue

            if not value_matcher.matches(value, matcher_error):
                # Be careful to only call add_traverse_path_step() for the first matcher failure.
                if not has_matcher_failed and matcher_error:
                    matcher_error.add_traverse_path_step(RTypeMatcherTraversePathStepEnum.Key, key)

                has_matcher_failed = True

            del dict_copy[key]

        # This looks weird at first sight.
        # It was done to reduce the scope of 'result',
        # and make intent of 'has_matcher_failed' clearer in the loop above.
        result = not has_matcher_failed
        error_message = ''

        if missing_key_set:
            if matcher_error:
                j = '], ['.join([RStrUtil.auto_quote(x) for x in missing_key_set])
                error_message = 'Missing keys: [{}]'.format(j)

            result = False

        # Tests if dict_copy has any remaining items
        if self.__is_exact and dict_copy:
            if matcher_error:
                if error_message:
                    error_message += '\n\t'

                error_message += 'Extra items: {}'.format(dict_copy)

            result = False

        if error_message and matcher_error:
            matcher_error.add_failed_match(self, d, RMessageText(error_message))

        return result

    __threadlocal = threading.local()

    # TODO: Make a threadlocal dict that works by enum -> factory lambda
    # Ref: http://stackoverflow.com/a/1408178/257299
    def __get_empty_threadlocal_missing_key_set(self) -> set:

        x = getattr(self.__threadlocal, 'missing_key_set', None)
        """:type: set"""

        if x is None:
            x = set()
            setattr(self.__threadlocal, 'missing_key_set', x)
        else:
            x.clear()

        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RDictWhereMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = ((self.__is_exact == other.__is_exact) and (self.__matcher_dict == other.__matcher_dict))
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash((self.__is_exact, self.__matcher_dict))
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self):
        where_clause = "EXACTLY" if self.__is_exact else "AT LEAST"
        x = RStrUtil.auto_quote_dict(self.__matcher_dict)
        y = "{} where {} {}".format(super().__str__(), where_clause, x)
        return y
