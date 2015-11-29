from rambutan3.check_args.base.RRestrictedInstanceMatcher import RRestrictedInstanceMatcher


# Class bool is a subclass of int in Python.
# Do not allow bool (True/False) to match int.
INT = RRestrictedInstanceMatcher(allowed_class_or_type_non_empty_tuple=(int,), not_allowed_class_or_type_iterable=(bool,))
