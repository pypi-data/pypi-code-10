from rambutan3.check_args.base.RRestrictedInstanceMatcher import RRestrictedInstanceMatcher


# noinspection PyPep8Naming
def RESTRICTED_INSTANCE_OF(*,
                           allowed_class_or_type_tuple: tuple,
                           not_allowed_class_or_type_tuple: tuple) -> RRestrictedInstanceMatcher:

    x = RRestrictedInstanceMatcher(allowed_class_or_type_non_empty_tuple=allowed_class_or_type_tuple,
                                   not_allowed_class_or_type_iterable=not_allowed_class_or_type_tuple)
    return x
