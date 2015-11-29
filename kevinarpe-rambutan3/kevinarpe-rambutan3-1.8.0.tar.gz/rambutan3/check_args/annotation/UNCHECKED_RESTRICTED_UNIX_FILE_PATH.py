from rambutan3.check_args.file.RFilePathTypeEnum import RFilePathTypeEnum
from rambutan3.check_args.file.RUncheckedRestrictedUnixFilePathMatcher import RUncheckedRestrictedUnixFilePathMatcher


# noinspection PyPep8Naming
def UNCHECKED_RESTRICTED_UNIX_FILE_PATH(*allowed_file_path_type_tuple: RFilePathTypeEnum):
    x = RUncheckedRestrictedUnixFilePathMatcher(*allowed_file_path_type_tuple)
    return x
