from rambutan3.check_args.base.RInstanceByTypeNameMatcher import RInstanceByTypeNameMatcher


# noinspection PyPep8Naming
def INSTANCE_BY_TYPE_NAME(type_name: str) -> RInstanceByTypeNameMatcher:
    x = RInstanceByTypeNameMatcher(type_name)
    return x
