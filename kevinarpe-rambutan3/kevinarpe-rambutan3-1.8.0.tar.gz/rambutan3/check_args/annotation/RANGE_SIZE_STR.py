from rambutan3.check_args.other.RRangeSizeStr import RRangeSizeStr


# noinspection PyPep8Naming
def RANGE_SIZE_STR(*, min_size: int=-1, max_size: int=-1):
    x = RRangeSizeStr(min_size=min_size, max_size=max_size)
    return x
